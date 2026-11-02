# Limbo Card Game - GUI Version

A complete graphical implementation of the Limbo card game for two players, featuring an intuitive mouse-driven interface and AI opponents. Developed as part of an Agile development project.

## Game Overview

Limbo is a strategic card game where players take turns playing cards to reduce a count starting from 101. The goal is to be the last player able to play a card without reducing the count below zero.

## Features

### 🎮 Gameplay Features
- **Full GUI Interface**: Beautiful graphical interface with mouse control
- **Human vs Human**: Two players on the same computer
- **Human vs AI**: Play against computer opponents with 3 difficulty levels
- **Complete Rule Implementation**: All Limbo card game rules faithfully implemented
- **Interactive Card Selection**: Click cards to play them with visual feedback
- **Action Selection**: Choose between multiple card effects when available

### 🎨 Visual Features
- **Animated Splash Screen**: Professional startup experience
- **Intuitive Card Display**: Clear card representations with suit symbols and colors
- **Real-time Game State**: Live count display with color-coded danger levels
- **Visual Feedback**: Card highlighting, selection states, and hover effects
- **Responsive Layout**: Adapts to different screen sizes

### 🤖 AI Features
- **Three Difficulty Levels**:
  - **Easy**: Basic moves, occasional mistakes, beginner-friendly
  - **Medium**: Good strategy, considers opponent moves, balanced challenge
  - **Hard**: Advanced strategy, multiple-move lookahead, very challenging
- **Intelligent Decision Making**: AI considers card effects, opponent options, and endgame strategy
- **Natural Gameplay**: AI thinks for realistic amounts of time

### ⚙️ Additional Features
- **Comprehensive Settings**: Customize gameplay, display, and AI preferences
- **Complete Rules Reference**: Built-in tutorial and strategy guide
- **Score Tracking**: Persistent scoring across multiple rounds
- **Doubling System**: Risk/reward mechanics for higher stakes
- **Settings Persistence**: Your preferences are saved between sessions

## Project Structure

```
limbo-gui/
├── main.py                    # Application entry point
├── requirements.txt           # Project dependencies  
├── README.md                 # This file
├── src/                      # Source code package
│   ├── core/                 # Core game logic
│   │   ├── __init__.py
│   │   ├── card.py           # Card class with GUI enhancements
│   │   ├── deck.py           # Deck management
│   │   ├── player.py         # Player class with GUI features
│   │   ├── ai_player.py      # AI opponent implementation
│   │   └── game_manager.py   # Game state and logic manager
│   └── gui/                  # GUI components
│       ├── __init__.py
│       ├── main_window.py    # Main application window
│       ├── splash_screen.py  # Startup splash screen
│       ├── menu_screen.py    # Main menu interface
│       ├── game_screen.py    # Game playing interface
│       ├── rules_screen.py   # Rules and tutorial screen
│       ├── settings_screen.py # Settings and preferences
│       ├── card_widget.py    # Individual card display
│       ├── action_dialog.py  # Card action selection
│       └── player_setup_dialog.py # Game setup dialog
```

## Installation and Setup

### Prerequisites
- **Python 3.7 or higher**
- **tkinter** (included with most Python installations)
- **Windows 10/11** (primary target platform)

### Windows Setup (Middlesex University Environment)
1. Ensure Python 3.7+ is installed with tkinter
2. Clone or extract the project files
3. Navigate to the project directory
4. Run the game:
   ```cmd
   python main.py
   ```

### Alternative Platforms

#### macOS:
```bash
python3 main.py
```

#### Linux (Ubuntu/Debian):
```bash
# Install tkinter if not available
sudo apt-get install python3-tk

# Run the game
python3 main.py
```

### Verifying Installation
The application should start with a splash screen, followed by the main menu. If you encounter any issues, ensure tkinter is properly installed.

## How to Play

### Starting a Game

1. **Launch the Application**: Run `python main.py`
2. **Choose Game Mode**:
   - **Human vs Human**: Two players sharing the same computer
   - **Human vs Computer**: Play against AI opponent
3. **Configure Game Settings**:
   - Enter player names
   - Set target score (default: 200 points)
   - Choose AI difficulty if playing against computer
4. **Start Playing**: Click "Start Game" to begin

### Game Interface

#### Game Screen Layout
- **Top Area**: Opponent's information and cards
- **Center Area**: Current count display and game information  
- **Bottom Area**: Your cards and information
- **Side Panel**: Game controls and quick rules reference

#### Playing Cards
1. **Select a Card**: Click on a card in your hand
2. **Choose Action**: If the card has multiple effects, select your preferred action
3. **Confirm Play**: Click "Play Selected Card" or double-click the card
4. **Visual Feedback**: Watch the count update and turn pass to opponent

### Game Rules Summary

#### Basic Rules
- Game starts with a count of 101
- Players take turns playing cards to reduce the count
- **Cannot let the count go below zero**
- Last player to successfully play a card wins the round

#### Card Effects

**Number Cards (2-10):**
- Can either subtract OR divide the count
- **Division is mandatory** if the number divides evenly into the current count

**Aces:**
- Count as either 1 or 11 (your choice)
- Can only subtract (not divide)

**Face Cards:**
- **Jack**: Repeats the effect of the previous card played
- **Queen**: Reverses the digits of the current count (only if it reduces the count)
- **King**: Divides the count by any chosen number >1 and <current count (no remainder)

#### Scoring
- **Winner**: 10 × number of cards played in the round
- **Loser**: 10 × final count value
- **Doubling**: Multiply winner's score by 2× (double) or 4× (redouble)
- **Game Winner**: First player to reach target score

### AI Opponents

#### Difficulty Levels

**Easy AI:**
- Makes basic strategic moves
- Occasionally makes suboptimal choices
- Great for learning the game
- Thinks quickly

**Medium AI:**
- Uses good strategy and tactics
- Considers opponent's possible moves
- Balanced and challenging gameplay
- Moderate thinking time

**Hard AI:**
- Advanced strategic planning
- Looks multiple moves ahead
- Creates strategic traps
- Challenging for experienced players
- Longer thinking time for realistic feel

## Settings and Customization

### Game Settings
- **Default Target Score**: Customize the winning score
- **Auto-play Stock**: Automatically play stock card when hand is empty
- **Action Confirmation**: Enable/disable confirmation dialogs
- **Strategy Tips**: Show helpful gameplay hints

### Display Settings
- **Animation Speed**: Control the speed of visual transitions
- **Visual Theme**: Choose from different color schemes
- **Card Back Color**: Customize the appearance of face-down cards
- **Card Hints**: Enable helpful tooltips on card hover

### AI Settings
- **Default Difficulty**: Set preferred AI challenge level
- **Behavior Customization**: Understand how each difficulty level plays

### Advanced Settings
- **Settings Import/Export**: Backup and restore your preferences
- **Reset to Defaults**: Restore original settings
- **Settings Location**: Find where your preferences are stored

## Development Notes

This is the **GUI version (Sprint 2)** of the Limbo game project. Key development features:

### Technical Implementation
- **Pure Python/tkinter**: No external dependencies required
- **Object-Oriented Design**: Clean separation of concerns with MVC architecture
- **Event-Driven Architecture**: Responsive to user interactions
- **State Management**: Robust game state handling with callbacks
- **Cross-Platform Compatibility**: Works on Windows (primary), macOS, and Linux

### Code Architecture
- **Modular Design**: Separate packages for core logic and GUI components
- **Extensible Framework**: Easy to add new features or modify existing ones
- **Clean Interfaces**: Well-defined APIs between components
- **Error Handling**: Graceful handling of edge cases and user errors

### GUI Design Principles
- **User-Friendly**: Intuitive interface requiring no technical knowledge
- **Visual Clarity**: Clear information display and visual feedback
- **Responsive Design**: Smooth interactions and appropriate feedback timing
- **Accessibility**: High contrast, clear fonts, and logical navigation

## Troubleshooting

### Common Issues

**"ImportError: No module named 'tkinter'"**
- **Windows**: Reinstall Python with tkinter option checked
- **macOS**: Use Python from python.org (not Homebrew)
- **Linux**: Install python3-tk package

**Application won't start**
- Verify Python version: `python --version` (should be 3.7+)
- Check if running from correct directory
- Ensure all source files are present

**Cards not displaying correctly**
- Check screen resolution and scaling settings
- Try different visual theme in settings
- Restart application

**AI moves too quickly/slowly**
- Adjust animation speed in display settings
- Note: AI thinking time is intentional for realism

**Settings not saving**
- Check file permissions in home directory
- Ensure sufficient disk space
- Try running as administrator (Windows)

### Windows-Specific Notes
- Tested on Windows 10/11 with default Python installation
- Should work with Middlesex University computing environment
- If screen scaling causes issues, try adjusting display settings

### Performance Tips
- Close other applications for smoother animations
- Reduce animation speed if experiencing lag
- Game is lightweight and should run on modest hardware

## Future Enhancements

Potential additions for future versions:
- **Network Multiplayer**: Play against remote opponents
- **Tournament Mode**: Bracket-style competitions
- **Advanced AI**: Even more sophisticated computer opponents
- **Sound Effects**: Audio feedback for game events
- **Card Images**: Custom artwork for cards
- **Game Statistics**: Detailed performance tracking
- **Replay System**: Review and analyze past games

## Technical Support

For technical issues or questions:

1. **Check Troubleshooting Section**: Most common issues are covered above
2. **Verify Requirements**: Ensure Python 3.7+ and tkinter are installed
3. **Test with Default Settings**: Reset settings to defaults if experiencing issues
4. **Check File Permissions**: Ensure the application can read/write settings

## License

This project is developed for educational purposes as part of an Agile development course assignment.

## Development Credits

- **Platform**: Python 3.7+ with tkinter GUI framework
- **Development Environment**: VS Code
- **Target Platform**: Windows (Middlesex University standard)
- **Architecture**: Object-oriented design with MVC pattern
- **AI Implementation**: Custom strategic algorithms with difficulty scaling

---

**Version**: 1.0 GUI Edition  
**Compatibility**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)  
**Last Updated**: 2025

Enjoy playing Limbo! 🎮