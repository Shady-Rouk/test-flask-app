// static/js/spotify_updater.js

/**
 * Fetches the latest Spotify "Now Playing" data from the Flask backend
 * and updates the relevant section of the HTML page.
 */
function updateSpotifyNowPlaying() {
    // Make a fetch request to the Flask endpoint for Spotify data
    fetch('/spotify-now-playing')
        .then(response => {
            // Check if the network response was successful (status 200-299)
            if (!response.ok) {
                // Log the error and throw it to be caught by the .catch block
                console.error('Network response was not ok:', response.status, response.statusText);
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }
            return response.json(); // Parse the JSON response body
        })
        .then(data => {
            // Get the container element where Spotify content will be displayed
            const spotifyDynamicContent = document.getElementById('spotify-dynamic-content');
            let htmlContent = ''; // Initialize a variable to hold the new HTML

            if (data.is_playing) {
                // If a track is currently playing, construct the HTML for the playing state
                htmlContent = `
                <div id="playing-content" class="w-full flex flex-col items-center">
                    <img id="album-art"
                        src="${data.album_art_url || 'https://placehold.co/150x150/EEEEEE/333333?text=No+Art'}"
                        alt="Album Art" class="w-36 h-36 rounded-lg shadow-md mb-4 object-cover border border-gray-300">

                    <div class="text-center w-full">
                        <a id="track-name-link" href="${data.track_url}" target="_blank"
                            rel="noopener noreferrer"
                            class="text-xl font-semibold text-gray-900 hover:text-spotifyGreen transition-colors duration-200 block truncate">${data.track_name}</a>
                        <p id="artist-name" class="text-gray-600 text-sm truncate">${data.artist_name}</p>
                        <p id="album-name" class="text-gray-500 text-xs mt-1 truncate">${data.album_name}
                        </p>
                    </div>
                </div>
            `;
            } else {
                // If nothing is playing, construct the HTML for the not playing state
                htmlContent = `
                <div id="not-playing-message" class="text-gray-600 text-center">
                    <p class="text-lg">${data.message || 'Nothing currently playing on Spotify.'}</p>
                    <p class="text-sm mt-2">Check back later!</p>
                </div>
            `;
            }
            // Update the inner HTML of the dynamic content container
            spotifyDynamicContent.innerHTML = htmlContent;
        })
        .catch(error => {
            // Log any errors that occurred during the fetch operation
            console.error('There was a problem fetching Spotify data:', error);
            // Get the container element for error display
            const spotifyDynamicContent = document.getElementById('spotify-dynamic-content');
            // Update the content to show an error message
            spotifyDynamicContent.innerHTML = `
            <div id="not-playing-message" class="text-gray-600 text-center">
                <p class="text-lg">Error loading Spotify data.</p>
                <p class="text-sm mt-2">Please try refreshing the page.</p>
            </div>
        `;
        });
}

// Ensure the DOM is fully loaded before trying to access elements
document.addEventListener('DOMContentLoaded', () => {
    // Call the function immediately when the page loads to display initial data
    updateSpotifyNowPlaying();

    // Set an interval to call the function every 10 seconds (10000 milliseconds)
    // This keeps the Spotify information updated periodically
    setInterval(updateSpotifyNowPlaying, 10000);
});
