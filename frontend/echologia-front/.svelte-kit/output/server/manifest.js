export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["robots.txt"]),
	mimeTypes: {".txt":"text/plain"},
	_: {
		client: {start:"_app/immutable/entry/start.CvD_x3QY.js",app:"_app/immutable/entry/app.BgSgupg-.js",imports:["_app/immutable/entry/start.CvD_x3QY.js","_app/immutable/chunks/CgpkcZn7.js","_app/immutable/chunks/DXRL32hh.js","_app/immutable/chunks/8KO6lHU_.js","_app/immutable/chunks/CebReTEO.js","_app/immutable/chunks/CBX89MFy.js","_app/immutable/entry/app.BgSgupg-.js","_app/immutable/chunks/8KO6lHU_.js","_app/immutable/chunks/CebReTEO.js","_app/immutable/chunks/DsnmJJEf.js","_app/immutable/chunks/DXRL32hh.js","_app/immutable/chunks/CBX89MFy.js","_app/immutable/chunks/BvOURHpg.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
