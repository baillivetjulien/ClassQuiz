<!--
SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie

SPDX-License-Identifier: MPL-2.0
-->

<!-- Agence fork: native HTML rendering of a simple slide on the host screen
     (layouts validated in the mockups, baillivetjulien/leohoot#41). -->
<script lang="ts">
	import type { AgenceSlide, AgenceSource } from '$lib/quiz_types';
	import MediaComponent from '$lib/editor/MediaComponent.svelte';
	import Sources from '$lib/agence/Sources.svelte';

	interface Props {
		slide: AgenceSlide;
		image?: string | null;
		sources?: AgenceSource[] | null;
	}

	let { slide, image = null, sources = null }: Props = $props();

	// Lines starting with a bullet become a list, the others stay paragraphs.
	const blocks = $derived(
		(slide.text ?? '')
			.split('\n')
			.map((line) => line.trim())
			.filter(Boolean)
			.map((line) => ({
				bullet: /^[•\-–]\s*/.test(line),
				text: line.replace(/^[•\-–]\s*/, '')
			}))
	);
	const layout = $derived(image || slide.layout === 'TEXT' ? slide.layout : 'TEXT');
</script>

<div class="agence-slide" data-layout={layout}>
	{#if layout === 'BIG_IMAGE'}
		{#if slide.title}<h2 class="titre centre">{slide.title}</h2>{/if}
		<div class="grande-image">
			<MediaComponent
				src={image}
				css_classes="max-h-full max-w-full object-contain rounded-xl"
				muted={false}
			/>
		</div>
	{:else if layout === 'TITLE_TEXT_IMAGE'}
		<div class="colonnes">
			<div class="illustration">
				<MediaComponent
					src={image}
					css_classes="max-h-full max-w-full object-contain rounded-2xl shadow-lg"
					muted={false}
				/>
			</div>
			<div class="texte">
				{#if slide.title}<h2 class="titre">{slide.title}</h2>{/if}
				{@render corps()}
			</div>
		</div>
	{:else}
		<div class="texte seul">
			{#if slide.title}<h2 class="titre">{slide.title}</h2>{/if}
			{@render corps()}
		</div>
	{/if}
	<Sources {sources} variante="ecran" />
</div>

{#snippet corps()}
	{#each blocks as block, i (i)}
		{#if block.bullet}
			<p class="puce">{block.text}</p>
		{:else}
			<p>{block.text}</p>
		{/if}
	{/each}
{/snippet}

<style>
	.agence-slide {
		height: calc(100vh - 8rem);
		padding: 1.5rem 3rem 2rem;
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		color: var(--color-agence-encre);
	}
	.titre {
		font-size: clamp(1.75rem, 3.6vw, 3.6rem);
		font-weight: 800;
		line-height: 1.1;
		color: var(--color-agence-indigo-fonce);
		margin-bottom: 1rem;
	}
	.titre.centre {
		text-align: center;
		margin-bottom: 0;
	}
	.grande-image {
		flex: 1;
		min-height: 0;
		background: #fff;
		border-radius: 1.75rem;
		box-shadow: 0 6px 24px rgb(58 69 120 / 0.12);
		padding: 1.25rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.grande-image :global(img),
	.grande-image :global(video),
	.illustration :global(img),
	.illustration :global(video) {
		max-height: 100%;
		max-width: 100%;
		object-fit: contain;
	}
	.colonnes {
		flex: 1;
		min-height: 0;
		display: grid;
		grid-template-columns: 1.1fr 1fr;
		gap: 3rem;
		align-items: center;
	}
	.illustration {
		height: 100%;
		min-height: 0;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.texte {
		font-size: clamp(1.25rem, 2.2vw, 2.1rem);
		line-height: 1.45;
		overflow: hidden;
	}
	.texte.seul {
		flex: 1;
		max-width: 75rem;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		justify-content: center;
		text-align: center;
	}
	.texte p + p {
		margin-top: 0.6rem;
	}
	.puce {
		position: relative;
		padding-left: 1.6em;
		text-align: left;
	}
	.puce::before {
		content: '';
		position: absolute;
		left: 0.35em;
		top: 0.55em;
		width: 0.5em;
		height: 0.5em;
		border-radius: 50%;
		background: var(--color-agence-magenta);
	}
</style>
