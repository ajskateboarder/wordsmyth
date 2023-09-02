#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use tauri::api::process::Command;

#[tauri::command]
async fn run_river() {    
  let _ = Command::new("chmod")
  .args(["+x", "./river"])
  .output()
  .unwrap();
  let _ = Command::new("./river").spawn();
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![run_river])
        .run(tauri::generate_context![])
        .expect("error while running tauri application");
}
