<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { Question } from '$lib/quiz_types';
	import { onMount } from 'svelte';
	import Pikaso from 'pikaso';
	import SlideView from '$lib/agence/SlideView.svelte'; // Agence fork

	interface Props {
		question: Question;
	}

	let { question }: Props = $props();

	let canvas_el: HTMLDivElement | undefined = $state();
	let canvas: Pikaso;
	let img_src = $state('');

	onMount(async () => {
		if (question.slide) return; // Agence fork: native HTML slide, no canvas
		canvas = new Pikaso({
			container: canvas_el,
			snapToGrid: {},
			selection: {
				interactive: false
			}
		});
		if (typeof question.answers === 'string') {
			const data = JSON.parse(question.answers);
			// import.json() is async: it resolves once every image of the slide is loaded.
			// Exporting before that produced slides without their images.
			await canvas.import.json(data);
			img_src = canvas.export.toImage();
		}
	});
</script>

{#if question.slide}
	<SlideView slide={question.slide} image={question.image} />
{:else}
	<div class="w-full h-full">
		<div class="hidden">
			<div bind:this={canvas_el} class="w-full h-full block"></div>
		</div>
		<div class="w-full h-full flex justify-center">
			<img src={img_src} alt="Slide image" />
		</div>
	</div>
{/if}
