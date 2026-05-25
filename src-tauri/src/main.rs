#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use windows::core::PCWSTR;
use windows::Win32::System::Services::*;
use windows::Win32::Foundation::*;

fn to_wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

fn install_service() {
    let exe_dir = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .to_path_buf();

    let backend = exe_dir.join("mcpanel-backend.exe");
    let backend_str = backend.to_str().unwrap();

    unsafe {
        let scm = OpenSCManagerW(
            PCWSTR::null(),
            PCWSTR::null(),
            SC_MANAGER_CREATE_SERVICE,
        ).unwrap();

        let service_name = to_wide("mcPanelBackend");
        let binary_path = to_wide(backend_str);

        let svc = CreateServiceW(
            scm,
            PCWSTR(service_name.as_ptr()),
            PCWSTR(service_name.as_ptr()),
            SERVICE_ALL_ACCESS,
            SERVICE_WIN32_OWN_PROCESS,
            SERVICE_AUTO_START,
            SERVICE_ERROR_NORMAL,
            PCWSTR(binary_path.as_ptr()),
            PCWSTR::null(),
            None,
            PCWSTR::null(),
            PCWSTR::null(),
            PCWSTR::null(),
        ).unwrap();

        StartServiceW(svc, None).ok();
        CloseServiceHandle(svc).ok();
        CloseServiceHandle(scm).ok();
    }
}

fn service_is_running() -> bool {
    let output = std::process::Command::new("sc")
        .args(["query", "mcPanelBackend"])
        .output();

    match output {
        Ok(o) => String::from_utf8_lossy(&o.stdout).contains("RUNNING"),
        Err(_) => false,
    }
}

fn main() {
    let _ = std::panic::catch_unwind(|| {
        if !service_is_running() {
            let start = std::process::Command::new("sc")
                .args(["start", "mcPanelBackend"])
                .output();

            if start.is_err() || !start.unwrap().status.success() {
                install_service();
            }
        }
    });

    mcpaneltauriappsv_lib::run();
}