<!--
SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie

SPDX-License-Identifier: MPL-2.0
-->

<!-- Navigation bar of the Agence fork: replaces the upstream marketing navbar. -->
<script lang="ts">
	import { signedIn, pathname } from '$lib/stores';
	import { APP_NAME, LOGO_WHITE } from '$lib/agence/config';
</script>

<nav class="agence-nav fixed top-0 z-30 w-screen">
	<div class="mx-auto flex h-16 items-center gap-4 px-4 lg:px-10">
		<a href="/" class="flex items-center gap-3 text-white">
			<img
				src={LOGO_WHITE}
				alt="Agence de l'orientation — Région Normandie"
				class="h-11 w-auto"
			/>
			<span class="hidden text-lg font-semibold sm:inline">{APP_NAME}</span>
		</a>
		<div class="ml-auto flex items-center gap-1 sm:gap-2">
			<a class="agence-nav-link" href="/play">Rejoindre une partie</a>
			{#if $signedIn}
				<a class="agence-nav-link" href="/dashboard">Mes quiz</a>
				<a class="agence-nav-link" href="/api/v1/users/logout">Se déconnecter</a>
			{:else}
				<a class="agence-nav-link agence-nav-cta" href="/account/login?returnTo={$pathname}"
					>Espace conseillère</a
				>
			{/if}
		</div>
	</div>
</nav>

<style>
	.agence-nav {
		background: var(--color-agence-indigo);
		box-shadow: 0 2px 12px rgb(58 69 120 / 0.25);
	}
	.agence-nav-link {
		color: #fff;
		font-weight: 600;
		padding: 0.5rem 0.9rem;
		border-radius: 999px;
		white-space: nowrap;
		transition: background-color 0.2s;
	}
	.agence-nav-link:hover,
	.agence-nav-link:focus-visible {
		background: rgb(255 255 255 / 0.16);
	}
	.agence-nav-cta {
		background: var(--color-agence-magenta);
	}
	.agence-nav-cta:hover,
	.agence-nav-cta:focus-visible {
		background: #a80264;
	}
</style>
