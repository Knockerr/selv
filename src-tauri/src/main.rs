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
    fn preload_system_wayland() {
        if std::env::var_os("APPIMAGE").is_none() {
            return;
        }
        let candidates = [
            "/usr/lib/libwayland-client.so.0", // Arch-based
            "/usr/lib/x86_64-linux-gnu/libwayland-client.so.0", // Debian / Ubuntu
            "/usr/lib64/libwayland-client.so.0", // Fedora / openSUSE
        ];
        if let Some(path) = candidates.iter().find(|p| std::path::Path::new(p).exists()) {
            let new = match std::env::var("LD_PRELOAD") {
                Ok(old) if !old.is_empty() => format!("{path}:{old}"),
                _ => path.to_string(),
            };
            unsafe { std::env::set_var("LD_PRELOAD", new) };
        }
    }

    #[cfg(target_os = "linux")]
    {
        preload_system_wayland();
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
