<!--
SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie

SPDX-License-Identifier: MPL-2.0
-->

<!-- Footer of the Agence fork. Keeps the MPL 2.0 source link required by the licence. -->
<script lang="ts">
	import { APP_NAME, ORGANISATION, SOURCE_URL, UPSTREAM_URL } from '$lib/agence/config';
</script>

<footer class="agence-footer">
	<p><strong>{APP_NAME}</strong> · {ORGANISATION}</p>
	<p>
		Aucune donnée personnelle n'est demandée aux participants.
		<a href={SOURCE_URL} target="_blank" rel="noopener">Code source (licence MPL 2.0)</a>,
		version adaptée de <a href={UPSTREAM_URL} target="_blank" rel="noopener">ClassQuiz</a>.
	</p>
</footer>

<style>
	.agence-footer {
		margin-top: 3rem;
		padding: 1.5rem 1rem 2rem;
		text-align: center;
		font-size: 0.875rem;
		line-height: 1.6;
		color: var(--color-agence-encre-douce);
		border-top: 1px solid var(--color-agence-bord);
	}
	.agence-footer a {
		color: var(--color-agence-indigo-fonce);
		text-decoration: underline;
	}
</style>
