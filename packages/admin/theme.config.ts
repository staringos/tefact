
let colors = {
	primary: '#7367F0',
	success: '#28C76F',
	danger: '#EA5455',
	warning: '#FF9F43',
	dark: '#1E1E1E',
}

// CONFIGS
const themeConfig = {
	theme: 'light',						        // options[String]: 'light'(default), 'dark', 'semi-dark'
	sidebarCollapsed: false,			    // options[Boolean]: true, false(default)
	navbarColor: "#fff",				      // options[String]: HEX color / rgb / rgba / Valid HTML Color name - (default: #fff)
	navbarType: "floating",				    // options[String]: floating(default) / static / sticky / hidden
	footerType: "static",				      // options[String]: static(default) / sticky / hidden
	routerTransition: 'zoom-fade',		// options[String]: zoom-fade / slide-fade / fade-bottom / fade / zoom-out / none(default)
	disableCustomizer: false,			    // options[Boolean]: true, false(default)
	hideScrollToTop: false,				    // options[Boolean]: true, false(default)
	disableThemeTour: false,					// options[Boolean]: true, false(default)
}

export default themeConfig
