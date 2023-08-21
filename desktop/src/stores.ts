import { writable } from "svelte/store";

export let email = writable(localStorage.getItem("email") ?? "");
export let password = writable(localStorage.getItem("password") ?? "");
