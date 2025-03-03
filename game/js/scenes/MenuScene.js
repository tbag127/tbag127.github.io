class MenuScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MenuScene' });
    }

    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // Title
        const title = this.add.text(width / 2, height / 4, 'Super Forbidden Game', { 
            fontFamily: 'Arial', 
            fontSize: '48px', 
            color: '#ffffff',
            stroke: '#000000',
            strokeThickness: 6
        });
        title.setOrigin(0.5);
        
        // Subtitle
        const subtitle = this.add.text(width / 2, height / 4 + 60, 'A Puzzle Adventure', { 
            fontFamily: 'Arial', 
            fontSize: '24px', 
            color: '#ffffff',
            stroke: '#000000',
            strokeThickness: 4
        });
        subtitle.setOrigin(0.5);
        
        // Start button
        const startButton = this.add.text(width / 2, height / 2 + 50, 'Start Game', { 
            fontFamily: 'Arial', 
            fontSize: '32px', 
            color: '#ffffff',
            backgroundColor: '#880000',
            padding: { x: 20, y: 10 }
        });
        startButton.setOrigin(0.5);
        startButton.setInteractive({ useHandCursor: true });
        
        // Button hover effect
        startButton.on('pointerover', () => {
            startButton.setStyle({ backgroundColor: '#aa0000' });
        });
        
        startButton.on('pointerout', () => {
            startButton.setStyle({ backgroundColor: '#880000' });
        });
        
        // Start game on click
        startButton.on('pointerdown', () => {
            this.scene.start('Level1Scene');
        });
        
        // Instructions
        const instructions = this.add.text(width / 2, height - 100, 
            'Use arrow keys or touch controls to move\nPress SPACE or tap action button to use powers', { 
            fontFamily: 'Arial', 
            fontSize: '18px', 
            color: '#ffffff',
            align: 'center'
        });
        instructions.setOrigin(0.5);
        
        // Add some animation to the title
        this.tweens.add({
            targets: title,
            y: title.y - 10,
            duration: 1500,
            ease: 'Sine.easeInOut',
            yoyo: true,
            repeat: -1
        });
    }
}
