<script lang="ts">
	import { Search, Play, Pause } from 'lucide-svelte';
    import { goto } from '$app/navigation';	

	interface AudioFile {
		id: number;
		filename: string;
		date: string;
		labels: string[];
		criticality: number;
	}

	let searchQuery = $state('');
	let playingId: number | null = $state(null);
	let hoveredRow: number | null = $state(null);

	const audioFiles: AudioFile[] = [
		{
			id: 1,
			filename: 'Rec.001.wav',
			date: 'Apr, 12, 2025',
			labels: ['Persona Recognition', 'Max Mustermann'],
			criticality: 5
		},
		{
			id: 2,
			filename: 'movie.mp4',
			date: 'Apr, 12, 2025',
			labels: ['Commander conversation', 'Background activity'],
			criticality: 3
		},
		{
			id: 3,
			filename: 'Mustermann.mp3',
			date: 'Apr, 12, 2025',
			labels: ['Persona Recognition', 'Max Mustermann'],
			criticality: 2
		},
		{
			id: 4,
			filename: 'Train_Noises.wav',
			date: 'Apr, 12, 2025',
			labels: ['Location Identification', 'Niu-York', 'Train noises'],
			criticality: 2
		},
		{
			id: 5,
			filename: 'Nice-river-sounds.mp3',
			date: 'Apr, 12, 2025',
			labels: ['Noises', 'River'],
			criticality: 1
		}
	];

	let filteredFiles: AudioFile[] = $state([]);

	function updateFilteredFiles() {
		filteredFiles = audioFiles.filter(file =>
			file.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
			file.labels.some(label => label.toLowerCase().includes(searchQuery.toLowerCase()))
		);
	}

	$effect(() => {
		updateFilteredFiles();
	});

	$effect(() => {
		searchQuery;
		updateFilteredFiles();
	});

    function handlePlay(id: number) {
        playingId = playingId === id ? null : id;
    }

    function handleRowClick(id: number) {
        goto(`/player?fileId=${id}`);
    }

	function getRowClass(fileId: number): string {
		const baseClass =
			'grid grid-cols-12 gap-4 px-6 py-5 transition-all duration-300 cursor-pointer';
		const hoverClass = hoveredRow === fileId ? 'bg-slate-700/30 scale-[1.01]' : 'hover:bg-slate-700/20';
		return `${baseClass} ${hoverClass}`;
	}

	function getIndicatorClass(fileId: number): string {
		const baseClass = 'w-2 h-2 rounded-full transition-all duration-300';
		const statusClass = playingId === fileId ? 'bg-cyan-400 animate-pulse' : 'bg-slate-600';
		return `${baseClass} ${statusClass}`;
	}

	function getCriticalityColor(level: number): string {
		switch (level) {
			case 1:
				return 'text-green-400';
			case 2:
				return 'text-yellow-400';
			case 3:
				return 'text-yellow-500';
			case 4:
				return 'text-orange-400';
			case 5:
				return 'text-red-400';
			default:
				return 'text-slate-400';
		}
	}

	function getCriticalityBgColor(level: number): string {
		switch (level) {
			case 1:
				return 'bg-green-500/20';
			case 2:
				return 'bg-yellow-500/20';
			case 3:
				return 'bg-yellow-600/20';
			case 4:
				return 'bg-orange-500/20';
			case 5:
				return 'bg-red-500/20';
			default:
				return 'bg-slate-700/20';
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
	<div class="max-w-6xl mx-auto">
		<!-- Header -->
		<div class="mb-12 animate-fadeIn">
			<div class="flex items-center gap-3 mb-8">
				<div class="relative">
					<div class="w-12 h-12 rounded-full bg-cyan-500 flex items-center justify-center animate-pulse">
						<div class="w-8 h-8 rounded-full border-4 border-white"></div>
					</div>
					<div class="absolute inset-0 w-12 h-12 rounded-full bg-cyan-400 animate-ping opacity-20"></div>
				</div>
				<h1 class="text-4xl font-bold text-white">Echologia</h1>
			</div>

			<!-- Search Bar -->
			<div class="relative group">
				<Search class="absolute left-4 top-1/2 transform -translate-y-1/2 text-cyan-400 w-5 h-5 transition-all group-hover:scale-110" />
				<input
					type="text"
					placeholder="Search anything..."
					bind:value={searchQuery}
					class="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-4 pl-12 pr-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:bg-slate-800/80 transition-all duration-300 backdrop-blur-sm"
				/>
			</div>
		</div>

		<!-- Table -->
		<div class="bg-slate-800/30 backdrop-blur-md rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl">
			<!-- Table Header -->
            <div class="grid grid-cols-12 gap-4 px-6 py-4 bg-slate-800/50 border-b border-slate-700/50">
				<div class="col-span-2 text-slate-400 text-sm font-semibold tracking-wider uppercase">
                    Criticality
                </div>
                <div class="col-span-3 text-slate-400 text-sm font-semibold tracking-wider uppercase">
                    File Name
                </div>
                <div class="col-span-2 text-slate-400 text-sm font-semibold tracking-wider uppercase">
                    Date
                </div>
                <div class="col-span-4 text-slate-400 text-sm font-semibold tracking-wider uppercase">
                    Labels
                </div>
                <div class="col-span-1 text-slate-400 text-sm font-semibold tracking-wider uppercase">
                    Actions
                </div>
            </div>

			<!-- Table Body -->
			<div class="divide-y divide-slate-700/30">
                {#each filteredFiles as file, index (file.id)}
                    <div
                        class={getRowClass(file.id)}
                        on:mouseenter={() => (hoveredRow = file.id)}
                        on:mouseleave={() => (hoveredRow = null)}
                        on:click={() => handleRowClick(file.id)}
                        style="animation: slideIn 0.5s ease-out {index * 0.1}s both"
                    >

				 <!-- Criticality -->
                           <div class="col-span-2 flex items-center">
                            <div class={`px-3 py-2 rounded-lg ${getCriticalityBgColor(file.criticality)} flex items-center gap-2`}>
                                <span class={`text-sm font-semibold ${getCriticalityColor(file.criticality)}`}>
                                    {file.criticality}/5
                                </span>
                            </div>
                        </div>
                        <!-- Filename -->
                        <div class="col-span-3 flex items-center gap-3">
                            <span class="text-slate-200 font-medium">{file.filename}</span>
                        </div>

                        <!-- Date -->
                        <div class="col-span-2 flex items-center text-slate-400">
                            {file.date}
                        </div>

                        <!-- Labels -->
                        <div class="col-span-4 flex flex-wrap gap-2 items-center">
                            {#each file.labels as label, idx (idx)}
                                <span
                                    class="px-3 py-1 bg-slate-700/50 text-cyan-300 text-sm rounded-full border border-slate-600/50 transition-all duration-300 hover:bg-slate-600/50 hover:scale-105"
                                    style="animation: fadeIn 0.5s ease-out {index * 0.1 + idx * 0.05}s both"
                                >
                                    {label}
                                </span>
                            {/each}
                        </div>
                        <!-- Actions -->
                        <div class="col-span-1 flex items-center gap-2">
                            <button
                                on:click|stopPropagation={() => handlePlay(file.id)}
                                class="p-2 rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 transition-all duration-300 hover:scale-110"
                            >
                                {#if playingId === file.id}
                                    <Pause class="w-4 h-4" />
                                {:else}
                                    <Play class="w-4 h-4" />
                                {/if}
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
		</div>

		<!-- Stats Footer -->
		<div class="mt-8 flex justify-between items-center text-slate-400 text-sm">
			<div class="flex gap-6">
				<span class="flex items-center gap-2">
					<div class="w-2 h-2 rounded-full bg-cyan-400"></div>
					{filteredFiles.length} recordings
				</span>
				<span class="flex items-center gap-2">
					<div class="w-2 h-2 rounded-full bg-green-400"></div>
					All synced
				</span>
			</div>
			<div>Last updated: Today</div>
		</div>
	</div>
</div>

<style>
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	:global(.animate-fadeIn) {
		animation: fadeIn 0.8s ease-out;
	}
</style>
