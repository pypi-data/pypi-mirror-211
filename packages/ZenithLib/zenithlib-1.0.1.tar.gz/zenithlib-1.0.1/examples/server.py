import Zenith


app = Zenith.WApp()

homePageContent = Zenith.getDotZenith('./page.zenith')

builder = Zenith.Builder({"home": homePageContent})
built = builder.Build()

style = Zenith.Stylesheet.new({
    'body': {
        'overflow': 'hidden',
        'background-color': '#f8f9fa',
        'font-family': 'Arial, sans-serif',
    },
    'id.container': {
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '100vh',
        'background-color': '#f8f9fa',
    },
    '.term': {
        'padding': '32px',
        'background-color': '#ffffff',
        'border-radius': '8px',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        'animation': 'fade-in 1s ease-in-out',
        'max-width': '500px',
        'text-align': 'center',
    },
    '.logo-container': {
        'display': 'flex',
        'justify-content': 'center',
        'margin-bottom': '16px',
    },
    '.term-title': {
        'font-size': '48px',
        'font-weight': 'bold',
        'margin-bottom': '16px',
        'color': '#007BFF',
        'text-decoration': 'none',
    },
    '.term-description': {
        'font-size': '24px',
        'font-style': 'italic',
        'color': '#6c757d',
        'margin-bottom': '16px',
    },
    '.term-definition': {
        'font-size': '20px',
        'color': '#343a40',
        'margin-bottom': '16px',
    },
    '.button-container': {
        'display': 'flex',
        'justify-content': 'center',
    },
    '.term-button': {
        'font-size': '20px',
        'padding': '8px 16px',
        'border': 'none',
        'border-radius': '4px',
        'background-color': '#007BFF',
        'color': '#ffffff',
        'cursor': 'pointer',
        'transition': 'background-color 0.3s ease',
        'margin': '0 8px',
        'text-decoration': 'none',
    },
    '.term-button:hover': {
        'background-color': '#0056b3',
    },
    '@keyframes fade-in': {
        '0%': {
            'opacity': '0',
            'transform': 'translateY(20px)',
        },
        '100%': {
            'opacity': '1',
            'transform': 'translateY(0)',
        },
    },
})



style.apply(built, "home")

app.register_route('/', built['home'])

app.serve()