<script lang="ts">
	import { goto } from '$app/navigation';
</script>

<div class="flex items-center gap-3 mb-8 cursor-pointer" onclick={() => goto('/')}>
	<div class="relative">
		<div class="w-12 h-12 rounded-full bg-cyan-500 flex items-center justify-center animate-pulse">
			<div class="w-8 h-8 rounded-full border-4 border-white"></div>
		</div>
		<div class="absolute inset-0 w-12 h-12 rounded-full bg-cyan-400 animate-ping opacity-20"></div>
	</div>
	<h1 class="text-4xl font-bold text-white">Echologia</h1>
</div>
