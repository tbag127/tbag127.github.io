/**
 * ResponsiveScale utility for Phaser games
 * Handles responsive scaling for different device sizes
 */
class ResponsiveScale {
    /**
     * Initialize responsive scaling
     * @param {Phaser.Game} game - The Phaser game instance
     */
    constructor(game) {
        this.game = game;
        this.setupResizeHandler();
    }
    
    /**
     * Set up the resize event handler
     */
    setupResizeHandler() {
        window.addEventListener('resize', () => {
            this.resizeGame();
        });
        
        // Initial resize
        this.resizeGame();
    }
    
    /**
     * Resize the game canvas based on window size
     */
    resizeGame() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        // Update game scale
        this.game.scale.resize(width, height);
        
        // Adjust UI elements based on screen size
        this.adjustUIForScreenSize(width, height);
    }
    
    /**
     * Adjust UI elements based on screen size
     * @param {number} width - Screen width
     * @param {number} height - Screen height
     */
    adjustUIForScreenSize(width, height) {
        // Get all active scenes
        const scenes = this.game.scene.scenes;
        
        scenes.forEach(scene => {
            // Only adjust UI for active scenes
            if (scene.scene.isActive()) {
                // Adjust camera
                if (scene.cameras && scene.cameras.main) {
                    // Adjust camera zoom based on screen size
                    if (width < 600) {
                        scene.cameras.main.setZoom(0.8);
                    } else {
                        scene.cameras.main.setZoom(1);
                    }
                }
                
                // Adjust UI elements if the scene has them
                if (scene.characterButtons) {
                    this.adjustCharacterButtons(scene, width, height);
                }
                
                // Adjust objective text if it exists
                if (scene.objectiveText) {
                    this.adjustObjectiveText(scene, width, height);
                }
            }
        });
    }
    
    /**
     * Adjust character selection buttons
     * @param {Phaser.Scene} scene - The scene containing the buttons
     * @param {number} width - Screen width
     * @param {number} height - Screen height
     */
    adjustCharacterButtons(scene, width, height) {
        const buttonY = height - 50;
        const buttonSpacing = width < 600 ? 70 : 100;
        
        scene.characterButtons.forEach((button, index) => {
            const x = 50 + (index * buttonSpacing);
            button.setPosition(x, buttonY);
            
            // Adjust text size based on screen width
            if (width < 400) {
                button.setFontSize(12);
                button.setPadding({ x: 5, y: 3 });
            } else if (width < 600) {
                button.setFontSize(14);
                button.setPadding({ x: 8, y: 4 });
            } else {
                button.setFontSize(16);
                button.setPadding({ x: 10, y: 5 });
            }
        });
    }
    
    /**
     * Adjust objective text
     * @param {Phaser.Scene} scene - The scene containing the text
     * @param {number} width - Screen width
     * @param {number} height - Screen height
     */
    adjustObjectiveText(scene, width, height) {
        scene.objectiveText.setPosition(width / 2, 100);
        
        // Adjust text size based on screen width
        if (width < 400) {
            scene.objectiveText.setFontSize(14);
            scene.objectiveText.setPadding({ x: 5, y: 3 });
        } else if (width < 600) {
            scene.objectiveText.setFontSize(16);
            scene.objectiveText.setPadding({ x: 8, y: 4 });
        } else {
            scene.objectiveText.setFontSize(18);
            scene.objectiveText.setPadding({ x: 10, y: 5 });
        }
    }
}
