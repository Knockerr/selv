import {
    mkdir,
    writeTextFile
} from "@tauri-apps/plugin-fs";
import {
    uiStore
} from "./components/bits-ui/uiComponentsStore.svelte";
import {
    appLocalDataDir,
    join,
    localDataDir
} from '@tauri-apps/api/path';

const logs = [];
const maxLogs = 5000;
let logDir;
let logPath;

function captureLog(level, args) {
    const logLine = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
    const entry = {
        level,
        timestamp: new Date().toISOString(),
        message: logLine
    };
    logs.push(entry);
    if (logs.length > maxLogs) logs.shift();

    if (level == "error"){
        uiStore.reportError(logLine)
        console.log("Reporting error " + logLine + " to user")
    }

    if (!logPath) return;
    writeTextFile(logPath, logLine + '\n', {
        append: true,
        create: true
    }).catch(e => originalError('Failed to write log:', e));
}


const originalLog = console.log;
const originalInfo = console.info;
const originalError = console.error;
const originalWarn = console.warn;

export async function init() {
    const baseDir = await localDataDir();
    logDir = await join(baseDir, "Selv", "App", "logs", "frontend");
    logPath = await join(logDir, "frontend.log")

    // Create file if not exists
    await mkdir(logDir, {
        recursive: true
    });

    // Catch errors
    window.addEventListener('error', (event) => {
        captureLog('error', [`[ ERROR ] Uncaught: ${event.message} at ${event.filename}:${event.lineno}`]);
        uiStore.reportError(`Uncaught: ${event.message} at ${event.filename}:${event.lineno}`)
    });

    window.addEventListener('unhandledrejection', (event) => {
        captureLog('error', [`[ ERROR ] Unhandled rejection: ${event.reason}`]);
        uiStore.reportError(`Unhandled rejection: ${event.reason}`)
    });

    console.log = (...args) => {
        captureLog('log', args);
        originalLog(...args);
    };
    console.info = (...args) => {
        captureLog('info', args);
        originalLog(...args);
    };
    console.error = (...args) => {
        captureLog('error', args);
        originalError(...args);
    };
    console.warn = (...args) => {
        captureLog('warn', args);
        originalWarn(...args);
    };
}