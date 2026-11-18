<!--
SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie

SPDX-License-Identifier: MPL-2.0
-->

<!-- Agence fork: source links of a slide or a question (baillivetjulien/leohoot#42).
     "ecran": compact chips at the bottom of the big screen; "telephone": clickable cards. -->
<script lang="ts">
	import type { AgenceSource } from '$lib/quiz_types';

	interface Props {
		sources?: AgenceSource[] | null;
		variante?: 'ecran' | 'telephone';
	}

	let { sources = [], variante = 'ecran' }: Props = $props();

	const domaine = (url: string): string => {
		try {
			return new URL(url).hostname.replace(/^www\./, '');
		} catch {
			return url;
		}
	};
	// Only http(s) links are rendered, even if the server already checked them.
	const liens = $derived((sources ?? []).filter((s) => /^https?:\/\//i.test(s.url)));
	const couleurs = ['#4d5a9b', '#cc0279', '#1f8f5b', '#3a4578', '#b05a00'];
</script>

{#if liens.length}
	{#if variante === 'ecran'}
		<div class="sources-ecran">
			<span class="intitule">Sources :</span>
			{#each liens as source (source.url)}
				<span class="pastille">
					<svg
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.5"
						aria-hidden="true"
						><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1" /><path
							d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"
						/></svg
					>
					{source.label}
					<small>{domaine(source.url)}</small>
				</span>
			{/each}
		</div>
	{:else}
		<div class="sources-telephone">
			{#each liens as source, i (source.url)}
				<a class="lien" href={source.url} target="_blank" rel="noopener noreferrer">
					<span class="icone" style="background:{couleurs[i % couleurs.length]}"
						>{domaine(source.url).charAt(0).toUpperCase()}</span
					>
					<span><b>{source.label}</b><small>{domaine(source.url)} ↗</small></span>
				</a>
			{/each}
		</div>
	{/if}
{/if}

<style>
	.sources-ecran {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: 0.75rem;
		font-size: clamp(1rem, 1.4vw, 1.4rem);
		color: var(--color-agence-encre-douce);
	}
	.intitule {
		font-weight: 600;
	}
	.pastille {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		background: #fff;
		border: 2px solid var(--color-agence-bord);
		border-radius: 999px;
		padding: 0.35rem 1rem;
		color: var(--color-agence-indigo-fonce);
		font-weight: 600;
	}
	.pastille svg {
		width: 1.1em;
		height: 1.1em;
		flex: none;
	}
	.pastille small {
		font-weight: 400;
		color: var(--color-agence-encre-douce);
	}
	.sources-telephone {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		width: 100%;
	}
	.lien {
		display: flex;
		align-items: center;
		gap: 0.85rem;
		background: #fff;
		border-radius: 1rem;
		padding: 0.85rem;
		box-shadow: 0 6px 24px rgb(58 69 120 / 0.12);
		text-align: left;
		color: var(--color-agence-encre);
	}
	.lien:focus-visible {
		outline: 4px solid var(--color-agence-turquoise);
	}
	.icone {
		width: 2.75rem;
		height: 2.75rem;
		border-radius: 0.75rem;
		display: grid;
		place-items: center;
		color: #fff;
		font-weight: 800;
		font-size: 1.25rem;
		flex: none;
	}
	.lien b {
		display: block;
		font-size: 1rem;
	}
	.lien small {
		color: var(--color-agence-indigo);
		font-size: 0.85rem;
	}
</style>
