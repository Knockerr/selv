// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;

fn install_service() {
    let nssm = "binaries/nssm.exe";
    // Recupere automatiquement le lien vers le exe du backend
    let backend = std::env::current_exe()
        .unwrap()
        .parent() 
        .unwrap()
        .join("mcpanel-backend.exe");

    // Installe le service
    Command::new(nssm)
        .args(["install", "mcPanelBackend", backend.to_str().unwrap()])
        .status().ok();

    // Configure le démarrage automatique
    Command::new(nssm)
        .args(["set", "mcPanelBackend", "Start", "SERVICE_AUTO_START"])
        .status().ok();

    // Démarre le service
    Command::new(nssm)
        .args(["start", "mcPanelBackend"])
        .status().ok();
}

fn main() {
    // Installe le service seulement si pas déjà installé
    let status = Command::new("sc")
        .args(["query", "mcPanelBackend"])
        .output();
    
    if status.is_err() || !status.unwrap().status.success() {
        install_service();
    }

    // Lance Tauri en dernier (bloquant)
    mcpaneltauriappsv_lib::run();
}