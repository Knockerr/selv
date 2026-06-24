// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
use std::process::Command;

const DETACHED_PROCESS: u32 = 0x00000008;
const CREATE_NEW_PROCESS_GROUP: u32 = 0x00000200;

fn main() {
    let mut path = std::env::current_exe().unwrap();
    path.pop();
    path.push("binaries");
    path.push("mcpanel-backend-x86_64-pc-windows-msvc.exe");

    let _ = Command::new("backend.exe")
        .creation_flags(DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        .spawn();

    mcpaneltauriappsv_lib::run()
}
