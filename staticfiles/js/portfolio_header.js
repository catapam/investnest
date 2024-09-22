/**
 * Adjusts the text color of the elements inside the portfolio header based on the background color.
 * If the background is light, text will be set to a darker color for contrast, and vice versa.
 */
function adjustTextColor() {
    const header = document.getElementById('portfolio-header');
    const bgColor = window.getComputedStyle(header).backgroundColor;

    // Get all child elements inside the header (h1, p, li, span)
    const children = header.querySelectorAll('h1, p, li, span');

    // Loop through each child element and adjust the text color
    children.forEach(function (child) {
        // Skip elements inside #portfolio-buttons to avoid unintended style changes
        if (child.closest('#portfolio-buttons')) return;

        // Check if the background color is light or dark and adjust text color accordingly
        if (isLightColor(bgColor)) {
            child.style.color = 'var(--bg-darker)'; // Use a dark color for light backgrounds
        } else {
            child.style.color = 'var(--text-primary-color)'; // Use a light color for dark backgrounds
        }
    });
}

/**
 * Converts RGB values to a luminance value.
 * Luminance helps determine if a color is light or dark.
 * @param {number} r - The red value (0-255).
 * @param {number} g - The green value (0-255).
 * @param {number} b - The blue value (0-255).
 * @returns {number} The calculated luminance value.
 */
function rgbToLuminance(r, g, b) {
    // Convert the RGB values to a relative scale
    let a = [r, g, b].map(function (v) {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });

    // Return the weighted sum of the luminance
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

/**
 * Converts a hex color code to its RGB equivalent.
 * @param {string} hex - The hex color code (e.g., #FFFFFF).
 * @returns {object} An object with the r, g, and b values (0-255).
 */
function hexToRgb(hex) {
    // Expand shorthand hex codes (e.g., #FFF) to full length (e.g., #FFFFFF)
    let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function (m, r, g, b) {
        return r + r + g + g + b + b;
    });

    // Extract the red, green, and blue values from the hex string
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

/**
 * Determines if a given color is light or dark based on its luminance.
 * @param {string} color - The color in either RGB or hex format.
 * @returns {boolean} True if the color is light, false if it is dark.
 */
function isLightColor(color) {
    let rgb;

    // Check if the color is provided in hex or RGB format
    if (color.startsWith('#')) {
        rgb = hexToRgb(color); // Convert hex to RGB
    } else if (color.startsWith('rgb')) {
        const values = color.match(/\d+/g); // Extract RGB values from the string
        rgb = {
            r: parseInt(values[0]),
            g: parseInt(values[1]),
            b: parseInt(values[2])
        };
    }

    // If RGB values are available, calculate luminance and determine if the color is light
    if (rgb) {
        const luminance = rgbToLuminance(rgb.r, rgb.g, rgb.b);
        return luminance > 0.5; // A luminance greater than 0.5 indicates a light color
    }
    return false; // Default to dark if no valid color is found
}

/**
 * Initializes the script after the DOM content has fully loaded.
 * Ensures the text color adjustment function is executed when the page is ready.
 */
document.addEventListener('DOMContentLoaded', function () {
    adjustTextColor();
});
