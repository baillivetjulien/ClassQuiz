// SPDX-FileCopyrightText: 2026 Agence régionale de l'orientation et des métiers de Normandie
//
// SPDX-License-Identifier: MPL-2.0

// Branding of the Agence fork. The public name is set at runtime with PUBLIC_APP_NAME
// (decision pending in baillivetjulien/leohoot#3), so it never needs a rebuild.
import { env } from '$env/dynamic/public';

export const APP_NAME: string = env.PUBLIC_APP_NAME || 'Quiz Orientation Normandie';
export const ORGANISATION = "Agence régionale de l'orientation et des métiers de Normandie";
export const SOURCE_URL = 'https://github.com/baillivetjulien/ClassQuiz';
export const UPSTREAM_URL = 'https://github.com/mawoka-myblock/ClassQuiz';
export const LOGO_WHITE = '/agence/logo-agence-blanc.png';

export const pageTitle = (page?: string): string => (page ? `${page} · ${APP_NAME}` : APP_NAME);
