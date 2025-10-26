<script lang="ts">
	import { page } from '$app/stores';
	import { Play, SkipForward, Volume2 } from 'lucide-svelte';
	import Header from './Header.svelte';

	let playbackSpeed = $state(1.5);

	const relatedRecordings = [
		{
			title: 'Aircraft landed',
			percentage: 30,
			details: ['BlackHawk', 'High Rank'],
			date: '10 May 25'
		},
		{
			title: 'Assault Advance',
			percentage: 70,
			details: ['Movement', 'Fire detected'],
			date: '10 May 25'
		}
	];

	const tags = ['Niu York', 'Indoor', 'High Rank', 'Minors detected'];

	const intelSummary = [
		'Immediate reaction advised.',
		'Direction Niu York.',
		'Heavy machinery, many drones type ABC-12',
		'Minors detected indoor'
	];

	const transcription = [
		{ time: '00:22', speaker: 'P2', text: 'South direction down th...' },
		{ time: '00:22', speaker: 'P1', text: 'Warm. Machinery movem...' },
		{ time: '00:22', speaker: 'P2', text: 'Cold' }
	];

	function togglePlaybackSpeed() {
		playbackSpeed = playbackSpeed === 1.5 ? 1 : 1.5;
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
	<div class="max-w-7xl mx-auto">
		<!-- Header -->
		<div class="mb-8">
			<Header />
		</div>

		<main>
		<div class="grid gap-6 lg:grid-cols-[1fr_400px]">
			<!-- Left Column -->
			<div class="space-y-6">
				<!-- Commander Conversation -->
				<div class="rounded-2xl border border-slate-700/50 bg-slate-800/30 p-6 backdrop-blur-md">
					<h2 class="mb-6 text-xl font-semibold uppercase tracking-wide text-slate-200">
						Commander Ccconversation
					</h2>

					<div class="space-y-6">
						<!-- Personnel Cards - Stacked Vertically -->
						<div class="space-y-4">
							<!-- Mustermann -->
                                <div class="flex items-center gap-4 rounded-lg bg-slate-700/30 p-4">
                                    <img
                                        src="/assets/commander.png"
                                        alt="Mustermann"
                                        class="h-20 w-20 rounded-lg object-cover bg-slate-600/50"
                                        onerror={(e) => {
                                            e.currentTarget.style.display = 'none';
                                        }}
                                    />
                                    <div class="flex-1 space-y-2">
                                        <div class="text-sm font-medium text-slate-400">Mustermann</div>
                                        <div class="grid grid-cols-3 gap-2 text-xs">
                                            <div>
                                                <div class="text-xs text-slate-500">AGE</div>
                                                <div class="font-medium text-slate-200">20-30</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-500">SEX</div>
                                                <div class="font-medium text-slate-200">Male</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-500">RANK</div>
                                                <div class="font-medium text-yellow-500">Private</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

							<!-- P2 Commander -->
                                <div class="flex items-center gap-4 rounded-lg bg-slate-700/30 p-4">
                                    <img
                                        src="/assets/unknown.png"
                                        alt="P2"
                                        class="h-20 w-20 rounded-lg object-cover bg-slate-600/50"
                                        onerror={(e) => {
                                            e.currentTarget.style.display = 'none';
                                        }}
                                    />
                                    <div class="flex-1 space-y-2">
                                        <div class="text-sm font-medium text-slate-400">P2</div>
                                        <div class="grid grid-cols-3 gap-2 text-xs">
                                            <div>
                                                <div class="text-xs text-slate-500">AGE</div>
                                                <div class="font-medium text-slate-200">30-45</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-500">SEX</div>
                                                <div class="font-medium text-slate-200">Male</div>
                                            </div>
                                            <div>
                                                <div class="text-xs text-slate-500">RANK</div>
                                                <div class="font-medium text-red-400">Commander</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

							<!-- Audio Player - Smaller -->
							<div class="rounded-lg bg-slate-700/30 p-4">
								<div class="mb-3 flex items-center justify-center">
									<svg class="h-10 w-full" viewBox="0 0 800 64">
										{#each Array.from({ length: 100 }) as _, i}
											{@const height = Math.random() * 50 + 10}
											<rect
												x={i * 8}
												y={32 - height / 2}
												width="4"
												height={height}
												fill={i < 30 ? 'rgb(34, 211, 238)' : 'rgb(71, 85, 105)'}
												opacity={i < 30 ? 1 : 0.5}
											/>
										{/each}
									</svg>
								</div>

								<div class="flex items-center justify-center gap-3">
									<button class="text-cyan-400 hover:text-cyan-300 transition-colors">
										<Play class="h-5 w-5" />
									</button>
									<button
										onclick={togglePlaybackSpeed}
										class="text-xs font-medium text-slate-200 hover:text-cyan-400 transition-colors"
									>
										{playbackSpeed}x
									</button>
									<button class="text-cyan-400 hover:text-cyan-300 transition-colors">
										<SkipForward class="h-5 w-5" />
									</button>
									<button class="text-cyan-400 hover:text-cyan-300 transition-colors">
										<Volume2 class="h-5 w-5" />
									</button>
								</div>
							</div>

							<!-- Transcription -->
							<div class="rounded-lg bg-slate-700/30 p-4">
								<div class="mb-3 text-sm font-medium text-slate-400">Transcription</div>
								<div class="space-y-2 text-sm">
									{#each transcription as item}
										<div class="flex gap-3">
											<span class="text-slate-500">{item.time}</span>
											<span class="text-slate-200">{item.speaker}: {item.text}</span>
										</div>
									{/each}
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Related Recordings -->
				<div class="rounded-2xl border border-slate-700/50 bg-slate-800/30 p-6 backdrop-blur-md">
					<h2 class="mb-6 text-xl font-semibold uppercase tracking-wide text-slate-200">
						Related Recordings
					</h2>

					<div class="grid gap-4 md:grid-cols-2">
						{#each relatedRecordings as recording}
							<div
								class="rounded-lg bg-slate-700/30 p-4 transition-colors hover:bg-slate-700/40 cursor-pointer"
							>
								<div class="mb-3 flex items-start justify-between">
									<h3 class="text-lg font-semibold text-slate-200">{recording.title}</h3>
									<div class="text-right">
										<div
											class={`text-2xl font-bold ${recording.percentage >= 50 ? 'text-red-400' : 'text-cyan-400'}`}
										>
											{recording.percentage} %
										</div>
									</div>
								</div>

								<div class="space-y-2">
									{#each recording.details as detail}
										<div class="text-sm text-slate-400">
											{detail}
										</div>
									{/each}
									<div class="pt-2 text-xs text-slate-500">{recording.date}</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Right Column - Threat Assessment -->
			<div>
				<div class="rounded-2xl border border-slate-700/50 bg-slate-800/30 p-6 backdrop-blur-md">
					<h2 class="mb-6 text-xl font-semibold uppercase tracking-wide text-slate-200">
						Threat Assessment
					</h2>

					<div class="space-y-8">
						<!-- Circular Gauge -->
						<div class="flex justify-center">
							<div class="relative h-48 w-48">
								<svg class="h-full w-full -rotate-90" viewBox="0 0 200 200">
									<!-- Background circle -->
									<circle
										cx="100"
										cy="100"
										r="80"
										fill="none"
										stroke="rgb(51, 65, 85)"
										stroke-width="16"
									/>
									<!-- Progress circle -->
									<circle
										cx="100"
										cy="100"
										r="80"
										fill="none"
										stroke="rgb(248, 113, 113)"
										stroke-width="16"
										stroke-dasharray={`${80 * 2 * Math.PI * 0.8} ${80 * 2 * Math.PI}`}
										stroke-linecap="round"
									/>
								</svg>
								<div class="absolute inset-0 flex flex-col items-center justify-center">
									<div class="text-5xl font-bold text-slate-200">80%</div>
									<div class="text-sm font-medium uppercase tracking-wide text-red-400">Critical</div>
								</div>
							</div>
						</div>

						<!-- Metrics -->
						<div class="space-y-3">
							<div class="flex justify-between text-sm">
								<span class="text-slate-400">CONFIDENCE</span>
								<span class="font-medium text-slate-200">87%</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-slate-400">RISK SCORE</span>
								<span class="font-medium text-slate-200">50%</span>
							</div>
						</div>

						<!-- Tags -->
						<div>
							<h3 class="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-200">Tags</h3>
							<div class="flex flex-wrap gap-2">
								{#each tags as tag}
									<span class="rounded-md bg-slate-700/30 px-3 py-1.5 text-sm text-slate-200">
										{tag}
									</span>
								{/each}
							</div>
						</div>

						<!-- Intel Summary -->
						<div>
							<h3 class="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-200">
								Intel Summary:
							</h3>
							<ul class="space-y-2 text-sm text-slate-200">
								{#each intelSummary as item}
									<li class="flex gap-2">
										<span class="text-cyan-400">•</span>
										<span>{item}</span>
									</li>
								{/each}
							</ul>
						</div>
					</div>
				</div>
			</div>
		</div>
	</main>
</div>