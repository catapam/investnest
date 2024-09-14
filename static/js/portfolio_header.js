// Function to adjust text color based on background color
function adjustTextColor() {
    const header = document.getElementById('portfolio-header');
    const bgColor = window.getComputedStyle(header).backgroundColor;

    // Get all child elements inside the header
    const children = header.querySelectorAll('h1, p, li, span');

    // Loop through each child element and adjust the text color
    children.forEach(function(child) {
        // Skip elements that are inside #portfolio-buttons
        if (child.closest('#portfolio-buttons')) return;

        // Check if the background color is light
        if (isLightColor(bgColor)) {
            child.style.color = 'var(--bg-darker)'; // Set to a darker color for light backgrounds
        } else {
            child.style.color = 'var(--text-primary-color)'; // Keep the text white for dark backgrounds
        }
    });
}

// Function to convert RGB to luminance value
function rgbToLuminance(r, g, b) {
    let a = [r, g, b].map(function(v) {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

// Function to convert hex to RGB
function hexToRgb(hex) {
    let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function(m, r, g, b) {
        return r + r + g + g + b + b;
    });
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

// Function to determine if a color is light or dark
function isLightColor(color) {
    let rgb;

    // Check if the color is in hex or rgb format
    if (color.startsWith('#')) {
        rgb = hexToRgb(color);
    } else if (color.startsWith('rgb')) {
        const values = color.match(/\d+/g);
        rgb = {
            r: parseInt(values[0]),
            g: parseInt(values[1]),
            b: parseInt(values[2])
        };
    }

    if (rgb) {
        const luminance = rgbToLuminance(rgb.r, rgb.g, rgb.b);
        return luminance > 0.5; // If luminance is greater than 0.5, it's a light color
    }
    return false; // Default to false if no valid color is found
}

document.addEventListener('DOMContentLoaded', function() {
    adjustTextColor();
});
