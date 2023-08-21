#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use serde_json::Value;
use reqwest::blocking::Client;
use reqwest::header;

use std::io;
use std::fs::File;
use std::process::{Command, Stdio};

fn get_river_url() -> Result<(String, String), Box<dyn std::error::Error>> {
    let url = "https://api.github.com/repos/ajskateboarder/river/releases/latest";
    let user_agent = header::HeaderValue::from_static("random bot");
    let client = Client::new();

    let response = client.get(url).header(header::USER_AGENT, user_agent).send()?;

    if response.status().is_success() {
        let json_response: Value = response.json()?;
        let assets = json_response["assets"].as_array().unwrap();
        let download_url: String;
        if cfg!(windows) {
            download_url = assets[1]["browser_download_url"].as_str().unwrap().to_string();
        } else {
            download_url = assets[0]["browser_download_url"].as_str().unwrap().to_string();
        }
        Ok((download_url.clone(), download_url.split("/").collect::<Vec<_>>().last().unwrap().to_string()))
    } else {
        Err("heyyy".into())
    }
}

fn download_file(url: (String, String)) {
    let resp = reqwest::blocking::get(url.0).expect("request failed");
    let body = resp.bytes().expect("body invalid");
    let mut out = File::create(url.1).expect("failed to create file");
    let body_bytes = body.to_vec();
    io::copy(&mut &body_bytes[..], &mut out).expect("failed to copy content");
}

fn main() {
    let url = get_river_url().unwrap();
    download_file(url);
    if !cfg!(windows) {
        let _ = Command::new("sh")
            .args(["-c", "chmod +x ./main; ./main &"]).stdout(Stdio::null()).stderr(Stdio::null()).spawn();
    }

    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
