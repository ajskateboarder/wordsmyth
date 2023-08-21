#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use std::{vec};

use tauri::api::process::Command;
use scraper::{Html, Selector};
use serde::{Deserialize, Serialize};

#[tauri::command]
async fn run_river() {    
  let _ = Command::new("chmod")
  .args(["+x", "./river"])
  .output()
  .unwrap();
  let _ = Command::new("./river").spawn();
}

#[derive(Serialize, Deserialize, Debug)]
struct AmazonResult {
    title: String,
    asin: String,
    rating: String,
    price: String,
    image: String,
    review_count: String,
}

#[tauri::command]
async fn search_results(
    html: String,
) -> Result<Vec<AmazonResult>, String> {
    let cards = Selector::parse("div[class=a-section]").unwrap();
    let fallback_cards = Selector::parse("div[class='a-section a-spacing-base']").unwrap();
    let title_links = Selector::parse(
        ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style .a-text-normal",
    )
    .unwrap();
    let rating = Selector::parse(".a-row.a-size-small span").unwrap();
    let price = Selector::parse(".a-price").unwrap();
    let image = Selector::parse(".s-image").unwrap();
    let review_count = Selector::parse(".a-size-base .s-underline-text").unwrap();

    let document = Html::parse_document(&html);

    let mut found_cards = document.select(&cards).collect::<Vec<_>>();
    found_cards = found_cards.split_last().unwrap().1.to_vec();

    if found_cards.len() == 0 {
        found_cards = document.select(&fallback_cards).collect::<Vec<_>>();
        found_cards = found_cards.split_last().unwrap().1.to_vec();
    }

    let mut amazon_results: Vec<AmazonResult> = vec![];

    for product in found_cards {
        let _title_link: Vec<_> = product.select(&title_links).collect::<Vec<_>>();

        if _title_link.len() == 0 {
            let _ = search_results(html.clone());
        }

        let mut title_link = _title_link[0];
        let title_text = title_link.text().collect::<String>();
        if title_text == "Sponsored" {
            continue;
        };
        if title_text == "" {
            title_link = product
                .select(&title_links)
                .filter(|item| item.text().collect::<String>() != "")
                .collect::<Vec<_>>()[1];
        }

        let binding = product.select(&rating).collect::<Vec<_>>();
        let select_rating: _ = binding.get(0);
        let mut final_rating = "None".to_string();

        if select_rating != None {
            final_rating = select_rating
                .unwrap()
                .value()
                .attr("aria-label")
                .unwrap_or("What")
                .to_string()
        }

        let binding = product.select(&price).collect::<Vec<_>>();
        let select_price: _ = binding.get(0);
        let mut final_price = "None".to_string();

        if select_price != None {
            final_price = select_price
                .unwrap()
                .text()
                .collect::<String>()
                .replace("\n", ".")
                .split_off(1)
                .split("$")
                .collect::<Vec<_>>()[0]
                .to_string();
        }

        amazon_results.push(AmazonResult {
            title: title_link.text().collect::<String>(),
            asin: title_link
                .value()
                .attr("href")
                .unwrap_or("None")
                .to_string(),
            rating: final_rating,
            price: final_price,
            image: product.select(&image).collect::<Vec<_>>()[0]
                .value()
                .attr("src")
                .unwrap_or("None")
                .to_string(),
            review_count: product.select(&review_count).collect::<Vec<_>>()[0]
                .text()
                .collect::<String>()
                .to_string(),
        })
    }

    Ok(amazon_results)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![run_river, search_results])
        .run(tauri::generate_context![])
        .expect("error while running tauri application");
}
