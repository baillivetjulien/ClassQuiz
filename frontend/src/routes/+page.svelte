<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie

SPDX-License-Identifier: MPL-2.0
-->

<!-- Agence fork: the upstream marketing landing page is replaced by two entry points. -->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { navbarVisible } from '$lib/stores.svelte.ts';
	import Footer from '$lib/footer.svelte';
	import { APP_NAME, pageTitle } from '$lib/agence/config';

	navbarVisible.visible = true;

	let pin = $state('');
	const pinValide = $derived(/^\d{6}$/.test(pin.replace(/\s/g, '')));

	const rejoindre = (e: SubmitEvent) => {
		e.preventDefault();
		if (pinValide) goto(`/play?pin=${pin.replace(/\s/g, '')}`);
	};
</script>

<svelte:head>
	<title>{pageTitle()}</title>
	<meta
		name="description"
		content="Quiz en direct pour les ateliers de l'Agence de l'orientation."
	/>
	<meta name="robots" content="noindex" />
</svelte:head>

<main class="accueil">
	<section class="intro">
		<h1>{APP_NAME}</h1>
		<p>Les quiz en direct des ateliers de l'Agence de l'orientation.</p>
	</section>

	<section class="entrees">
		<form class="carte" onsubmit={rejoindre}>
			<h2>Rejoindre une partie</h2>
			<p>Saisissez le code affiché sur le grand écran. Pas besoin de compte.</p>
			<label class="sr-only" for="pin">Code de la partie</label>
			<input
				id="pin"
				class="pin"
				bind:value={pin}
				inputmode="numeric"
				autocomplete="off"
				maxlength="7"
				placeholder="123 456"
			/>
			<button class="bouton bouton-principal" type="submit" disabled={!pinValide}
				>Rejoindre</button
			>
		</form>

		<div class="carte">
			<h2>Espace conseillère</h2>
			<p>Créer, modifier et animer les quiz des ateliers.</p>
			<a class="bouton bouton-secondaire" href="/account/login?returnTo=/dashboard"
				>Se connecter</a
			>
		</div>
	</section>
</main>

<Footer />

<style>
	.accueil {
		max-width: 64rem;
		margin: 0 auto;
		padding: 3rem 1rem 1rem;
	}
	.intro {
		text-align: center;
		margin-bottom: 2.5rem;
	}
	.intro h1 {
		font-size: clamp(2rem, 5vw, 3.25rem);
		font-weight: 800;
		color: var(--color-agence-indigo-fonce);
		line-height: 1.1;
	}
	.intro p {
		margin-top: 0.75rem;
		font-size: 1.25rem;
		color: var(--color-agence-encre-douce);
	}
	.entrees {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
		gap: 1.5rem;
	}
	.carte {
		background: #fff;
		border-radius: 1.75rem;
		box-shadow: 0 6px 24px rgb(58 69 120 / 0.12);
		padding: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	.carte h2 {
		font-size: 1.6rem;
		font-weight: 700;
		color: var(--color-agence-encre);
	}
	.carte p {
		color: var(--color-agence-encre-douce);
		line-height: 1.5;
	}
	.pin {
		font-size: 2.5rem;
		font-weight: 700;
		letter-spacing: 0.4rem;
		text-align: center;
		color: var(--color-agence-indigo);
		border: 3px solid var(--color-agence-bord);
		border-radius: 1rem;
		padding: 0.75rem;
		width: 100%;
	}
	.pin:focus {
		outline: none;
		border-color: var(--color-agence-indigo);
	}
	.bouton {
		display: block;
		text-align: center;
		border-radius: 999px;
		padding: 1rem;
		font-size: 1.25rem;
		font-weight: 700;
		margin-top: auto;
	}
	.bouton:focus-visible {
		outline: 4px solid var(--color-agence-turquoise);
		outline-offset: 2px;
	}
	.bouton-principal {
		background: var(--color-agence-magenta);
		color: #fff;
	}
	.bouton-principal:disabled {
		opacity: 0.45;
		cursor: not-allowed;
	}
	.bouton-secondaire {
		background: var(--color-agence-indigo);
		color: #fff;
	}
</style>
