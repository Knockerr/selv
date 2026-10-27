use tauri::Manager;

#[tauri::command]
fn set_window_icon(app: tauri::AppHandle, light: bool) -> Result<(), String> {
    let bytes: &[u8] = if light {
        include_bytes!("../icons/icon-light.png")
    } else {
        include_bytes!("../icons/icon-dark.png")
    };

    let decoded = image::load_from_memory(bytes)
        .map_err(|e| e.to_string())?
        .into_rgba8();

    let (width, height) = decoded.dimensions();

    let icon = tauri::image::Image::new_owned(decoded.into_raw(), width, height);

    let window = app
        .get_webview_window("main")
        .ok_or_else(|| "Fenêtre principale introuvable".to_string())?;

    window.set_icon(icon).map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_http::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_store::Builder::new().build())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![set_window_icon])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
