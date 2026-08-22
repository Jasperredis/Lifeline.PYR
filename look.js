function toggleFont() { document.documentElement.classList.toggle("cool-font") }
const THEMES = ['light', 'sand', 'ocean', 'watermelon', 'dark', 'demo', 'original'];
function setTheme(theme) {
	document.documentElement.classList.remove(...THEMES);
	document.documentElement.classList.add(theme);
}
