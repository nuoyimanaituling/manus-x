/**
 * Tool function mapping
 */
export const TOOL_FUNCTION_MAP: {[key: string]: string} = {
  // Shell tools
  "shell_exec": "Executing command",
  "shell_view": "Viewing command output",
  "shell_wait": "Waiting for command completion",
  "shell_write_to_process": "Writing data to process",
  "shell_kill_process": "Terminating process",
  
  // File tools
  "file_read": "Reading file",
  "file_write": "Writing file",
  "file_str_replace": "Replacing file content",
  "file_find_in_content": "Searching file content",
  "file_find_by_name": "Finding file",
  
  // Browser tools
  "browser_view": "Viewing webpage",
  "browser_navigate": "Navigating to webpage",
  "browser_restart": "Restarting browser",
  "browser_click": "Clicking element",
  "browser_input": "Entering text",
  "browser_move_mouse": "Moving mouse",
  "browser_press_key": "Pressing key",
  "browser_select_option": "Selecting option",
  "browser_scroll_up": "Scrolling up",
  "browser_scroll_down": "Scrolling down",
  "browser_console_exec": "Executing JS code",
  "browser_console_view": "Viewing console output",
  
  // Search tools
  "info_search_web": "Searching web",
  
  // Message tools
  "message_notify_user": "Sending notification",
  "message_ask_user": "Asking question",

  // Skill tools
  "load_skill": "Loading skill"
};

/**
 * Display name mapping for tool function parameters
 */
export const TOOL_FUNCTION_ARG_MAP: {[key: string]: string} = {
  "shell_exec": "command",
  "shell_view": "shell",
  "shell_wait": "shell",
  "shell_write_to_process": "input",
  "shell_kill_process": "shell",
  "file_read": "file",
  "file_write": "file",
  "file_str_replace": "file",
  "file_find_in_content": "file",
  "file_find_by_name": "path",
  "browser_view": "page",
  "browser_navigate": "url",
  "browser_restart": "url",
  "browser_click": "element",
  "browser_input": "text",
  "browser_move_mouse": "position",
  "browser_press_key": "key",
  "browser_select_option": "option",
  "browser_scroll_up": "page",
  "browser_scroll_down": "page",
  "browser_console_exec": "code",
  "browser_console_view": "console",
  "info_search_web": "query",
  "message_notify_user": "message",
  "message_ask_user": "question",
  "load_skill": "skill"
};

/**
 * Tool name mapping
 */
export const TOOL_NAME_MAP: {[key: string]: string} = {
  "shell": "Terminal",
  "file": "File",
  "browser": "Browser",
  "info": "Information",
  "message": "Message",
  "mcp": "MCP Tool",
  "skill": "Skill"
};

import SearchIcon from '../components/icons/SearchIcon.vue';
import EditIcon from '../components/icons/EditIcon.vue';
import BrowserIcon from '../components/icons/BrowserIcon.vue';
import ShellIcon from '../components/icons/ShellIcon.vue';
import SkillIcon from '../components/icons/SkillIcon.vue';

/**
 * Tool icon mapping
 */
export const TOOL_ICON_MAP: {[key: string]: any} = {
  "shell": ShellIcon,
  "file": EditIcon,
  "browser": BrowserIcon,
  "search": SearchIcon,
  "message": "",
  "mcp": SearchIcon,  // 暂时使用搜索图标，可以后续创建专门的MCP图标
  "skill": SkillIcon  // 书本图标，代表技能/知识
};

import ShellToolView from '@/components/toolViews/ShellToolView.vue';
import FileToolView from '@/components/toolViews/FileToolView.vue';
import SearchToolView from '@/components/toolViews/SearchToolView.vue';
import BrowserToolView from '@/components/toolViews/BrowserToolView.vue';
import McpToolView from '@/components/toolViews/McpToolView.vue';

/**
 * Mapping from tool names to components
 */
export const TOOL_COMPONENT_MAP: {[key: string]: any} = {
  "shell": ShellToolView,
  "file": FileToolView,
  "search": SearchToolView,
  "browser": BrowserToolView,
  "mcp": McpToolView
};
