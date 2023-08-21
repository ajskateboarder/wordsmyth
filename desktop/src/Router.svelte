<script lang="ts">
  import { Router, Route, Link } from "svelte-routing";
  import { email, password } from "./stores";

  import Modal from "./lib/Modal.svelte";
  import About from "./routes/Search.svelte";
  import Home from "./routes/Home.svelte";

  let showModal = false;
  let validPass = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($email);

  $: {
    const emailValue = localStorage.getItem("email");
    if (emailValue !== null) {
      email.set(emailValue);
    }
    const passwordValue = localStorage.getItem("password");
    if (passwordValue !== null) {
      password.set(passwordValue);
    }
    if (showModal === true) {
      validPass = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($email);
      (document.querySelector(".submit") as HTMLButtonElement).disabled =
        validPass;
    }
  }
  email.subscribe((value) => {
    localStorage.setItem("email", value);
  });
  password.subscribe((value) => {
    localStorage.setItem("password", value);
  });

  let url = "/";
</script>

<Router {url}>
  <div class="sidebar">
    <div class="top-icons">
      <Link to="/"><i class="fa fa-home sidebar-item" /></Link>
      <Link to="/about"><i class="fa fa-search sidebar-item" /></Link>
    </div>

    <div class="bottom-icons">
      <div class="sidebar-item">
        <a href="https://github.com" target="_blank">
          <img
            src="/github-mark-white.png"
            alt=""
            style="filter: padding: 20px"
            class="sidebar-item small-ass-item"
          />
        </a>
      </div>
      <i class="fa fa-cog sidebar-item" on:click={() => (showModal = true)} />
    </div>
  </div>
  <div class="views">
    <Route path="/about" component={About} />
    <Route path="/"><Home /></Route>
  </div>
</Router>

<Modal bind:showModal>
  <div slot="header">
    <h2>Account information</h2>
    <p style="color: var(--fg1)">
      Required to download Amazon reviews for analysis. This is never used
      anywhere except locally.
    </p>
  </div>
  <label for="Address">Username/email</label>
  <input type="email" name="Address" bind:value={$email} />
  {#if validPass}<i class="fa fa-times" />{:else}<i
      class="fa fa-check"
    />{/if}<br />
  <label for="Password">Password</label>
  <input type="password" name="Password" bind:value={$password} />
</Modal>

<style>
  .sidebar {
    width: 60px;
    background-color: var(--bg1);
    color: var(--fg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0px;
  }

  .small-ass-item {
    transform: scale(0.5);
  }

  :global(body) {
    font-family: "Rubik", sans-serif;
  }

  :global(a) {
    text-decoration: none;
    color: var(--fg);
  }

  .top-icons,
  .bottom-icons {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .top-icons {
    flex-grow: 1;
  }

  .sidebar-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .sidebar-item:hover {
    background-color: var(--bg2);
  }

  .views {
    margin-left: 60px;
    margin-top: 20px;
  }

  input {
    color: var(--fg);
  }
</style>
