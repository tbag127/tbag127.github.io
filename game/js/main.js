// Game configuration
const config = {
    type: Phaser.AUTO,
    parent: 'game-container',
    width: window.innerWidth,
    height: window.innerHeight,
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 300 },
            debug: false
        }
    },
    scene: [
        BootScene,
        MenuScene,
        Level1Scene,
        Level2Scene
    ],
    pixelArt: true,
    backgroundColor: '#000000',
    input: {
        activePointers: 3, // Support multi-touch
        smoothFactor: 0.2  // Smooth touch input
    }
};

// Create the game instance
const game = new Phaser.Game(config);

// Initialize responsive scaling
let responsiveScale;
game.events.once('ready', () => {
    responsiveScale = new ResponsiveScale(game);
});

// Mobile touch controls
document.addEventListener('DOMContentLoaded', function() {
    // Only setup touch controls if we're on a touch device
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        const leftBtn = document.getElementById('btn-left');
        const rightBtn = document.getElementById('btn-right');
        const actionBtn = document.getElementById('btn-action');
        const upBtn = document.getElementById('btn-up');
        const downBtn = document.getElementById('btn-down');
        
        // Global game controls state that scenes can access
        window.gameControls = {
            left: false,
            right: false,
            up: false,
            down: false,
            action: false
        };
        
        // Touch event handlers with improved touch handling
        const addTouchHandlers = (btn, control) => {
            // Prevent default touch behavior to avoid scrolling and zooming
            btn.addEventListener('touchstart', function(e) {
                e.preventDefault();
                window.gameControls[control] = true;
                
                // Add visual feedback
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
                this.style.transform = 'scale(0.95)';
            }, { passive: false });
            
            btn.addEventListener('touchend', function(e) {
                e.preventDefault();
                window.gameControls[control] = false;
                
                // Remove visual feedback
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
                this.style.transform = 'scale(1)';
            }, { passive: false });
            
            // Handle touch cancel (e.g., if finger moves out of button)
            btn.addEventListener('touchcancel', function(e) {
                window.gameControls[control] = false;
                
                // Remove visual feedback
                this.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
                this.style.transform = 'scale(1)';
            });
            
            // Handle touch move to allow continuous control
            btn.addEventListener('touchmove', function(e) {
                e.preventDefault();
                
                // Check if touch is still over the button
                const touch = e.touches[0];
                const rect = this.getBoundingClientRect();
                const isInside = 
                    touch.clientX >= rect.left && 
                    touch.clientX <= rect.right && 
                    touch.clientY >= rect.top && 
                    touch.clientY <= rect.bottom;
                
                window.gameControls[control] = isInside;
                
                // Update visual feedback
                if (isInside) {
                    this.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
                    this.style.transform = 'scale(0.95)';
                } else {
                    this.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
                    this.style.transform = 'scale(1)';
                }
            }, { passive: false });
        };
        
        // Add touch handlers to all control buttons
        addTouchHandlers(leftBtn, 'left');
        addTouchHandlers(rightBtn, 'right');
        addTouchHandlers(upBtn, 'up');
        addTouchHandlers(downBtn, 'down');
        addTouchHandlers(actionBtn, 'action');
    }
    
    // Set up character switching buttons for mobile
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        // Use the existing character switch buttons in the HTML
        const charButtons = [
            document.getElementById('char-btn-0'),
            document.getElementById('char-btn-1'),
            document.getElementById('char-btn-2')
        ];
        
        // Add event listeners to character buttons
        charButtons.forEach((btn, index) => {
            btn.addEventListener('touchstart', function(e) {
                e.preventDefault(); // Prevent default touch behavior
                
                // Update active character in the current scene
                if (game.scene.scenes) {
                    const activeScene = game.scene.scenes.find(s => s.scene.isActive);
                    if (activeScene && activeScene.switchCharacter) {
                        activeScene.switchCharacter(index);
                        
                        // Update button styles
                        charButtons.forEach((btn, i) => {
                            if (i === index) {
                                btn.classList.add('active');
                            } else {
                                btn.classList.remove('active');
                            }
                        });
                    }
                }
            });
        });
    }
});
