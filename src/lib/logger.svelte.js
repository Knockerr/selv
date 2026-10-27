import {
    mkdir,
    readTextFile,
    writeFile,
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
import JSZip from "jszip";
import { save } from "@tauri-apps/plugin-dialog";

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

    if (level == "error") {
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
    try {

        const baseDir = await localDataDir();
        logDir = await join(baseDir, "Selv", "logs", "frontend");
        logPath = await join(logDir, "frontend.log")

        // Create file if not exists
        await mkdir(logDir, {
            recursive: true
        });

    } catch (e) {
        originalError("Log init failed:", e);
        logPath = undefined;
    }

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


export async function getReport() {
    const zip = new JSZip();

    const content = await readTextFile(logPath);
    zip.file(`frontend/frontend.log`, content);

    const backendLogsResponse = await fetch(
        "http://localhost:40401/logs/download",
    );
    const backendLogsBlob = await backendLogsResponse.blob();
    const backendLogsBuffer = new Uint8Array(
        await backendLogsBlob.arrayBuffer(),
    );
    zip.file("backend/backend.log", backendLogsBuffer);

    const zipContent = await zip.generateAsync({
        type: "uint8array"
    });

    return zipContent;
}

export async function downloadReport() {
    const zipContent = await getReport();

    const savePath = await save({
        defaultPath: `selv_logs_${Date.now()}.zip`,
        filters: [{
            name: "Zip",
            extensions: ["zip"]
        }],
    });

    if (savePath) {
        await writeFile(savePath, zipContent);
    }
}