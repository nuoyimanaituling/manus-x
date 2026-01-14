import smtplib
import logging
import random
import asyncio
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict
from app.core.config import get_settings
from app.domain.external.cache import Cache
from app.application.errors.exceptions import BadRequestError

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending verification codes and notifications"""
    
    # Class variables
    VERIFICATION_CODE_PREFIX = "verification_code:"
    VERIFICATION_CODE_EXPIRY_SECONDS = 300  # 5 minutes
    
    def __init__(self, cache: Cache):
        self.settings = get_settings()
        self.cache = cache
    
    def _generate_verification_code(self) -> str:
        """Generate 6-digit verification code"""
        return f"{random.randint(100000, 999999)}"
    
    async def _store_verification_code(self, email: str, code: str) -> None:
        """Store verification code with expiration time in cache"""
        now = datetime.now()
        # Create verification code data
        code_data = {
            "code": code,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(seconds=self.VERIFICATION_CODE_EXPIRY_SECONDS)).isoformat(),
            "attempts": 0
        }
        
        # Store in cache with TTL
        key = f"{self.VERIFICATION_CODE_PREFIX}{email}"
        await self.cache.set(key, code_data, ttl=self.VERIFICATION_CODE_EXPIRY_SECONDS)
    
    async def verify_code(self, email: str, code: str) -> bool:
        """Verify if the provided code is valid for the email"""
        key = f"{self.VERIFICATION_CODE_PREFIX}{email}"
        
        # Get stored data from cache
        stored_data = await self.cache.get(key)
        if not stored_data:
            return False
        
        # Check if code has expired (cache TTL should handle this, but double-check)
        expires_at = datetime.fromisoformat(stored_data["expires_at"])
        if datetime.now() > expires_at:
            await self.cache.delete(key)
            return False
        
        # Check attempts limit (max 3 attempts)
        if stored_data["attempts"] >= 3:
            await self.cache.delete(key)
            return False
        
        # Increment attempt count
        stored_data["attempts"] += 1
        
        # Check if code matches
        if stored_data["code"] == code:
            # Remove the code after successful verification
            await self.cache.delete(key)
            return True
        
        # Update attempt count in cache
        remaining_ttl = int((expires_at - datetime.now()).total_seconds())
        if remaining_ttl > 0:
            await self.cache.set(key, stored_data, ttl=remaining_ttl)
        
        return False
    
    def _create_verification_email(self, email: str, code: str) -> MIMEMultipart:
        """Create verification email content"""
        msg = MIMEMultipart()
        msg['From'] = self.settings.email_from or self.settings.email_username
        msg['To'] = email
        msg['Subject'] = "Password Reset Verification Code"
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Password Reset Verification</h2>
            <p>You have requested to reset your password. Please use the following verification code:</p>
            <h3 style="color: #007bff; font-size: 24px; letter-spacing: 2px;">{code}</h3>
            <p><strong>This code will expire in 5 minutes.</strong></p>
            <p>If you did not request this password reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>AI Manus Team</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        return msg
    
    async def send_verification_code(self, email: str):
        """Send verification code to email address"""
        # Check if email configuration is available
        if not all([
            self.settings.email_host,
            self.settings.email_port,
            self.settings.email_username,
            self.settings.email_password
        ]):
            logger.error("Email configuration is incomplete, simulating email send")
            raise BadRequestError("Email configuration is incomplete")
        
        # Check if there's an existing verification code that's too recent
        key = f"{self.VERIFICATION_CODE_PREFIX}{email}"
        existing_data = await self.cache.get(key)
        if existing_data:
            try:
                # Check if the existing code was created less than 60 seconds ago
                created_at = datetime.fromisoformat(existing_data["created_at"])
                time_since_creation = (datetime.now() - created_at).total_seconds()
                
                if time_since_creation < 60:
                    remaining_wait = int(60 - time_since_creation)
                    raise BadRequestError(f"Please wait {remaining_wait} seconds before requesting a new verification code")
            except (KeyError, ValueError):
                # Invalid data, continue with new code generation
                pass
        
        # Generate verification code
        code = self._generate_verification_code()
        logger.debug(f"Generated verification code: {code}")
        
        # Create email message
        msg = self._create_verification_email(email, code)
        logger.debug(f"Created email message: {msg}")
        
        # Send email using SMTP
        await self._send_smtp_email(msg, email)

        # Store verification code
        await self._store_verification_code(email, code)
        
        logger.info(f"Verification code sent to {email}")
    
    async def _send_smtp_email(self, msg: MIMEMultipart, email: str) -> None:
        """Send email using SMTP (runs in thread pool to avoid blocking)"""
        logger.debug(f"Sending email to {email}")
        server = None
        try:
            # Create SMTP server connection
            logger.debug(f"Creating SMTP server connection to {self.settings.email_host}:{self.settings.email_port}")
            server = smtplib.SMTP_SSL(self.settings.email_host, self.settings.email_port)
            logger.debug(f"SMTP server created, {server}")
            result = server.login(self.settings.email_username, self.settings.email_password)
            logger.debug(f"SMTP server login result: {result}")
            
            # Send email
            text = msg.as_string()
            result = server.sendmail(msg['From'], email, text)
            logger.debug(f"SMTP server sendmail result: {result}")
        finally:
            if server:
                server.quit()
    
    async def cleanup_expired_codes(self) -> None:
        """Clean up expired verification codes - Cache TTL handles this automatically"""
        # Cache automatically handles expiration via TTL, so this method is mainly for manual cleanup

        # Get all verification code keys
        pattern = f"{self.VERIFICATION_CODE_PREFIX}*"
        keys = await self.cache.keys(pattern)

        expired_count = 0
        for key in keys:
            data = await self.cache.get(key)
            if data:
                try:
                    expires_at = datetime.fromisoformat(data["expires_at"])
                    if datetime.now() > expires_at:
                        await self.cache.delete(key)
                        expired_count += 1
                except (KeyError, ValueError):
                    # Invalid data, delete it
                    await self.cache.delete(key)
                    expired_count += 1

        if expired_count > 0:
            logger.info(f"Cleaned up {expired_count} expired verification codes")

    async def send_task_notification(
        self,
        to_email: str,
        task_name: str,
        result_summary: str,
        session_id: str,
        execution_time: Optional[datetime] = None
    ) -> None:
        """Send notification email after scheduled task execution

        Args:
            to_email: Recipient email address
            task_name: Name of the scheduled task
            result_summary: Summary of the execution result
            session_id: Session ID for viewing full details
            execution_time: When the task was executed
        """
        if not all([
            self.settings.email_host,
            self.settings.email_port,
            self.settings.email_username,
            self.settings.email_password
        ]):
            logger.warning("Email configuration incomplete, skipping task notification")
            return

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = self.settings.email_from or self.settings.email_username
        msg['To'] = to_email
        msg['Subject'] = f"定时任务完成: {task_name}"

        # Format execution time
        exec_time_str = execution_time.strftime("%Y-%m-%d %H:%M:%S") if execution_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get base URL from settings or use default
        base_url = getattr(self.settings, 'base_url', 'http://localhost:5173')

        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    定时任务执行完成
                </h2>

                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>任务名称:</strong> {task_name}</p>
                    <p style="margin: 5px 0;"><strong>执行时间:</strong> {exec_time_str}</p>
                </div>

                <h3 style="color: #2c3e50;">执行结果</h3>
                <div style="background-color: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
                    {result_summary}
                </div>

                <div style="margin-top: 20px;">
                    <a href="{base_url}/chat/{session_id}"
                       style="display: inline-block; background-color: #3498db; color: white;
                              padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        查看详情
                    </a>
                </div>

                <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
                <p style="color: #666; font-size: 12px;">
                    此邮件由 AI Manus 定时任务系统自动发送，请勿回复。
                </p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        try:
            await self._send_smtp_email(msg, to_email)
            logger.info(f"Task notification sent to {to_email} for task: {task_name}")
        except Exception as e:
            logger.error(f"Failed to send task notification to {to_email}: {e}")
            raise
