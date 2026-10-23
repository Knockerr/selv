#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;

fn main() {
    let mut path = std::env::current_exe().unwrap();
    path.pop();

    #[cfg(target_os = "windows")]
    {
        use std::os::windows::process::CommandExt;
        const CREATE_NO_WINDOW: u32 = 0x08000000;
        const CREATE_NEW_PROCESS_GROUP: u32 = 0x00000200;
        path.push("selv-backend.exe");
        let _ = Command::new(&path)
            .creation_flags(CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP)
            .spawn();
    }

    #[cfg(target_os = "linux")]
    {
        path.push("selv-backend");
        let r = Command::new(&path)
            .env_remove("LD_PRELOAD")
            .env_remove("LD_LIBRARY_PATH")
            .spawn();
        if let Err(e) = r {
            eprintln!("Backend spawn failed ({path:?}): {e}");
        }
    }

    selv_lib::run()
}
