import { writable } from "svelte/store";

export let email = writable(localStorage.getItem("email") ?? "");
export let password = writable(localStorage.getItem("password") ?? "");

type Review = {
  reviews: { reviewText: string; overall: number }[];
  meta: { title: string; image: string; rating: string };
  analyzed: any[];
  productId: string;
};

function check(asin: string) {
  if (localStorage.getItem(asin) === null) {
    localStorage.setItem(
      asin,
      JSON.stringify({ reviews: [], meta: [], analyzed: [], productId: asin })
    );
  }
}

export class ProductHandler {
  /** Saves a single review to a localStorage item */
  static saveReview(
    asin: string,
    data: { reviewText: string; overall: number }
  ) {
    check(asin);
    let existingReviews = this.read(asin)?.reviews;
    let reviews = [...(existingReviews as any[]), data];
    localStorage.setItem(
      asin,
      JSON.stringify({
        ...this.read(asin),
        reviews: reviews,
      })
    );
    return reviews;
  }
  /** Saves a single review analysis to a localStorage item */
  static saveAnalysis(asin: string, data: any) {
    check(asin);
    let existingAnalyses = this.read(asin)?.analyzed;
    let analyzed = [...(existingAnalyses as any[]), data];
    localStorage.setItem(
      asin,
      JSON.stringify({
        ...this.read(asin),
        analyzed: analyzed,
      })
    );
    return analyzed;
  }
  /** Saves extra product information to localStorage, such as the title and image */
  static saveProductInfo(asin: string, meta: Review["meta"]) {
    check(asin);
    let existingData = JSON.parse(localStorage.getItem(asin) as string);
    localStorage.setItem(
      asin,
      JSON.stringify({ ...existingData, meta: meta, productId: asin } as Review)
    );
  }
  static read(asin: string): Review | undefined {
    if (localStorage.getItem(asin) === null) {
      return undefined;
    }
    return JSON.parse(localStorage.getItem(asin) as string);
  }
  static fetchProducts(): Review[] {
    return Object.keys(localStorage)
      .filter((e) => !["password", "email", "a-font-class"].includes(e))
      .map((asin) => this.read(asin) as Review)
      .reverse();
  }
}

//@ts-ignore
globalThis.ProductHandler = ProductHandler;
