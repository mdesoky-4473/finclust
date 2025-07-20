import { isAuthenticated } from '$lib/stores/auth';

export function logout() {
	localStorage.removeItem('token');
	isAuthenticated.set(false);
}
