import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const isAuthenticated = writable(false);

if (browser) {
	isAuthenticated.set(!!localStorage.getItem('token'));
}
