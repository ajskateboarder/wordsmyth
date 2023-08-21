#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use serde_json::Value;
use reqwest::blocking::Client;
use reqwest::header;

fn download_river() -> Result<(), Box<dyn std::error::Error>> {
    let url = "https://api.github.com/repos/ajskateboarder/river/releases/latest";
    let user_agent = header::HeaderValue::from_static("random bot");
    let client = Client::new();

    let response = client.get(url).header(header::USER_AGENT, user_agent).send()?;

    if response.status().is_success() {
        let json_response: Value = response.json()?;
        for item in json_response["assets"].as_array().iter() {
            println!("{:?}", item)
        }
    } else {
        println!("Request was not successful: {:?}", response);
    }

    Ok(())
}

fn main() {
    let _ = download_river();

    // let save_file_path = "temp.zip";
    // let download_url = "https://github.com/Aaron009/temp_rust_web_download/raw/main/wwwroot/temp.zip";
    // let resp = reqwest::blocking::get(download_url).expect("request failed");
    // let body = resp.bytes().expect("body invalid");
    // let mut out = File::create(save_file_path).expect("failed to create file");
    // let body_bytes = body.to_vec();
    // io::copy(&mut &body_bytes[..], &mut out).expect("failed to copy content");

    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
