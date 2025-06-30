<script lang="ts">
	let users: any[] = [];

	async function fetchUsers() {
		const res = await fetch('http://localhost:8000/generate');
		const json = await res.json();
		users = json.data;
	}
</script>

<main class="p-4">
	<h1 class="text-2xl font-bold mb-4">FinClust: User Generator</h1>
	<button on:click={fetchUsers} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
		Generate Users
	</button>

	{#if users.length > 0}
		<table class="mt-6 w-full border text-sm">
			<thead>
				<tr class="bg-gray-100">
					<th class="p-2 border">Name</th>
					<th class="p-2 border">Age</th>
					<th class="p-2 border">Monthly Spend</th>
					<th class="p-2 border"># Txns</th>
					<th class="p-2 border">Savings</th>
				</tr>
			</thead>
			<tbody>
				{#each users as user}
					<tr>
						<td class="p-2 border">{user.name}</td>
						<td class="p-2 border">{user.age}</td>
						<td class="p-2 border">${user.monthly_spend}</td>
						<td class="p-2 border">{user.num_txns}</td>
						<td class="p-2 border">${user.savings}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
</main>
