// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
use std::process::Command;

#[cfg(target_os = "windows")]
const DETACHED_PROCESS: u32 = 0x00000008;
#[cfg(target_os = "windows")]
const CREATE_NEW_PROCESS_GROUP: u32 = 0x00000200;

fn main() {
    let mut path = std::env::current_exe().unwrap();
    path.pop();
    path.push("binaries");

    #[cfg(target_os = "windows")]
    path.push("mcpanel-backend-x86_64-pc-windows-msvc.exe");

    #[cfg(target_os = "linux")]
    path.push("mcpanel-backend-x86_64-unknown-linux-gnu");

    #[cfg(target_os = "windows")]
    let _ = Command::new(&path)
        .creation_flags(DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        .spawn();

    #[cfg(target_os = "linux")]
    let _ = Command::new(&path)
        .spawn();

    mcpaneltauriappsv_lib::run()
}