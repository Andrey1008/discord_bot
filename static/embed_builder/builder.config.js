/**
 * This script file will (or atleast should) run before the main script file runs.
 * This file should contain stuff like options, global variables (etc.) to be used by the main script.
 */

// Options
function utf8_to_b64( str ) {
    return encodeURIComponent(window.btoa(encodeURIComponent( str )));
}
// URL options can override the options below.
// Options set through the menu can override both until the page is refreshed.
options = {
    username: 'Гуляй Поле',
    avatar: 'https://cdn.discordapp.com/embed/avatars/1.png',
    verified: false,
    noUser: false,
    data: null,
    guiTabs: ['author', 'description'],
    useJsonEditor: false,
    reverseColumns: false,
    allowPlaceholders: false,
    autoUpdateURL: false,
    autoParams: false,
    hideEditor: true,
    hidePreview: false,
    hideMenu: true,
    single: false,
    noMultiEmbedsOption: false,
    sourceOption: false, // Display link to source code in menu.
}

// Default JSON object

// json = {
//     content: "Hello world",
//     embed: {
//         title: "A title",
//         description: "A description",
//     }
// }


// Write any code under the 'DOMContentLoaded' event to run after the page has loaded.
addEventListener('DOMContentLoaded', () => {
    // console.log('Hello 👋');
    console.log(window.data_embed)
    // Remove the colour picker
    // document.querySelector('.colors').remove()
})