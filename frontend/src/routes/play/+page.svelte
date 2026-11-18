<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<!--suppress ALL -->
<script lang="ts">
	import { pageTitle } from '$lib/agence/config'; // Agence fork
	import { socket } from '$lib/socket';
	import JoinGame from '$lib/play/join.svelte';
	import type { Answer, Question as QuestionType } from '$lib/quiz_types';
	import ShowTitle from '$lib/play/title.svelte';
	import Question from '$lib/play/question.svelte';
	import { navbarVisible } from '$lib/stores.svelte.ts';
	import ShowEndScreen from '$lib/play/admin/final_results.svelte';
	import KahootResults from '$lib/play/results_kahoot.svelte';
	import { getLocalization } from '$lib/i18n';
	import Cookies from 'js-cookie';
	import Sources from '$lib/agence/Sources.svelte'; // Agence fork
	const { t } = getLocalization();

	interface Props {
		// Exports
		data: any;
	}

	let { data }: Props = $props();
	let { game_pin } = $state(data);

	// Types
	interface GameMeta {
		started: boolean;
	}

	let game_mode = $state();
	let final_results: Array<null> | Array<Array<PlayerAnswer>> = $state([null]);

	interface PlayerAnswer {
		username: string;
		answer: string;
		right: string;
	}

	// Variables init
	let question_index = $state('');
	let unique = $state({});
	navbarVisible.visible = false;
	let answer_results: Array<Answer> = $state();
	let gameData = $state();
	let solution: QuestionType = $state();
	let username = $state('');
	let scores = $state({});
	let gameMeta: GameMeta = $state({
		started: false
	});

	let question: Question = $state();
	// Agence fork: slide shown on the big screen, with its sources (baillivetjulien/leohoot#42)
	let agence_slide: { title: string; sources: { label: string; url: string }[] } | undefined =
		$state(undefined);
	// `question` is typed with the Question component upstream; read its sources with the data type.
	const question_sources = $derived(
		(question as unknown as QuestionType | undefined)?.sources ?? []
	);

	let preventReload = true;

	// Functions
	function restart() {
		unique = {};
	}

	const confirmUnload = (event: Event) => {
		if (preventReload) {
			event.preventDefault();
			// eslint-disable-next-line @typescript-eslint/ban-ts-comment
			// @ts-ignore
			event.returnValue = '';
		}
	};

	socket.on('time_sync', (data) => {
		socket.emit('echo_time_sync', data);
	});

	socket.on('connect', async () => {
		console.log('Connected!');
		const cookie_data = Cookies.get('joined_game');
		if (!cookie_data) {
			return;
		}
		const data = JSON.parse(cookie_data);
		socket.emit('rejoin_game', {
			old_sid: data.sid,
			username: data.username,
			game_pin: data.game_pin
		});
		const res = await fetch(`/api/v1/quiz/play/check_captcha/${game_pin}`);
		const json = await res.json();
		game_mode = json.game_mode;
	});

	// Socket-events
	socket.on('joined_game', (data) => {
		gameData = data;
		// eslint-disable-next-line no-undef
		plausible('Joined Game', { props: { game_id: gameData.game_id } });
		Cookies.set('joined_game', JSON.stringify({ sid: socket.id, username, game_pin }), {
			expires: 3600
		});
	});
	socket.on('rejoined_game', (data) => {
		gameData = data;
		if (data.started) {
			gameMeta.started = true;
		}
	});

	socket.on('game_not_found', () => {
		const cookie_data = Cookies.get('joined_game');
		if (cookie_data) {
			Cookies.remove('joined_game');
			window.location.reload();
			return;
		}
	});

	socket.on('set_question_number', (data) => {
		agence_slide = undefined; // Agence fork
		solution = undefined;
		restart();
		question = data.question;
		question_index = data.question_index;
		answer_results = undefined;
	});

	// Agence fork: the host shows a slide; the phone shows its sources (leohoot#42)
	socket.on('agence_slide', (data) => {
		agence_slide = data;
		answer_results = undefined;
	});

	socket.on('start_game', () => {
		gameMeta.started = true;
	});

	socket.on('question_results', (data) => {
		restart();
		answer_results = data;
	});

	socket.on('username_already_exists', () => {
		window.alert('Username already exists!');
	});

	socket.on('kick', () => {
		window.alert('You got kicked');
		preventReload = false;
		game_pin = '';
		username = '';
		Cookies.set('kicked', 'value', { expires: 1 });
		window.location.reload();
	});
	socket.on('final_results', (data) => {
		final_results = data;
		Cookies.remove('joined_game');
	});

	socket.on('solutions', (data) => {
		solution = data;
	});

	let bg_color = $derived(gameData ? gameData.background_color : undefined);

	// The rest
</script>

<svelte:window onbeforeunload={confirmUnload} />
<svelte:head>
	<title>{pageTitle('Jouer')}</title>
</svelte:head>
<div
	class="min-h-screen min-w-full"
	style="background: {bg_color ? bg_color : 'transparent'}"
	class:text-black={bg_color}
>
	<div>
		{#if !gameMeta.started && gameData === undefined}
			<JoinGame bind:game_pin bind:game_mode bind:username />
		{:else if JSON.stringify(final_results) !== JSON.stringify([null])}
			<ShowEndScreen bind:data={scores} show_final_results={true} {username} />
		{:else if agence_slide}
			<!-- Agence fork: slide on the big screen, its sources on the phone -->
			<div class="flex flex-col items-center gap-4 p-6 text-center max-w-md mx-auto">
				<h2 class="text-2xl font-bold">{agence_slide.title}</h2>
				{#if agence_slide.sources.length}
					<p class="text-lg">Pour aller plus loin :</p>
					<Sources sources={agence_slide.sources} variante="telephone" />
				{/if}
				<p class="text-lg opacity-80">Regardez le grand écran.</p>
			</div>
		{:else if gameData !== undefined && question_index === ''}
			<ShowTitle
				title={gameData.title}
				description={gameData.description}
				cover_image={gameData.cover_image}
			/>
		{:else if gameMeta.started && gameData !== undefined && question_index !== '' && answer_results === undefined}
			{#key unique}
				<div class="text-black dark:text-black">
					<Question bind:game_mode bind:question {question_index} {solution} />
				</div>
			{/key}
		{:else if gameMeta.started && answer_results !== undefined}
			{#if answer_results === null}
				<div class="w-full flex justify-center">
					<h1 class="text-3xl">{$t('admin_page.no_answers')}</h1>
				</div>
			{:else}
				<div>
					<h2 class="text-center text-3xl mb-8">{$t('words.result', { count: 2 })}</h2>
				</div>
				{#key unique}
					<KahootResults {username} question_results={answer_results} bind:scores />
				{/key}
				<!-- Agence fork: the question's sources, once the answer is revealed -->
				{#if question_sources.length}
					<div class="max-w-md mx-auto p-4">
						<Sources sources={question_sources} variante="telephone" />
					</div>
				{/if}
			{/if}
		{/if}
	</div>
</div>
