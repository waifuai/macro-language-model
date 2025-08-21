from manim import *
import numpy as np

class WaifuChatbotExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Waifu Chatbot Architecture", font_size=48, color=BLUE)
        subtitle = Text("A Modular AI-Powered Conversation System", font_size=32, color=BLUE_B)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Core Architecture Overview
        self.show_architecture_overview()

        # Personality System
        self.explain_personality_system()

        # Conversation Modes
        self.explain_modes()

        # AI Integration
        self.explain_ai_integration()

        # Provider Abstraction
        self.explain_provider_system()

        # Data Flow
        self.show_data_flow()

        # Conclusion
        self.show_conclusion()

    def show_architecture_overview(self):
        # Main components as rectangles
        main_rect = Rectangle(width=12, height=8, color=BLUE, fill_opacity=0.1)

        # Core components
        core_label = Text("Waifu Chatbot Core", font_size=28, color=BLUE)
        core_label.move_to(main_rect.get_top() + UP * 0.5)

        # Main modules
        modules = VGroup(
            Text("CLI Interface", font_size=20, color=GREEN),
            Text("Main Controller", font_size=20, color=YELLOW),
            Text("Personality System", font_size=20, color=PINK),
            Text("Mode Management", font_size=20, color=ORANGE),
            Text("AI Integration", font_size=20, color=PURPLE),
            Text("Provider Abstraction", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(main_rect.get_center())

        self.play(Create(main_rect), Write(core_label))
        self.play(Write(modules))
        self.wait(3)
        self.play(FadeOut(main_rect), FadeOut(core_label), FadeOut(modules))

    def explain_personality_system(self):
        title = Text("Personality System", font_size=36, color=PINK)
        title.move_to(DOWN)
        self.play(Write(title))

        # Personality types
        personalities = VGroup(
            Text("Deredere (Loving)", font_size=20, color=RED),
            Text("Tsundere (Tsun-Tsun)", font_size=20, color=BLUE),
            Text("Kuudere (Cool)", font_size=20, color=GREEN),
            Text("Yandere (Yandere)", font_size=20, color=PURPLE),
            Text("Dandere (Shy)", font_size=20, color=ORANGE),
            Text("Himedere (Princess)", font_size=20, color=PINK)
        ).arrange(DOWN, aligned_edge=LEFT)

        # Personality configuration
        config_box = Rectangle(width=4, height=3, color=PINK, fill_opacity=0.2)
        config_label = Text("Personality Config", font_size=16, color=PINK)
        config_label.move_to(config_box.get_center())

        # Response generation
        response_box = Rectangle(width=4, height=3, color=PINK, fill_opacity=0.2)
        response_label = Text("Response Generation", font_size=16, color=PINK)
        response_label.move_to(response_box.get_center())

        config_box.move_to(LEFT * 3)
        response_box.move_to(RIGHT * 3)
        personalities.move_to(UP * 2)

        arrow = Arrow(config_box.get_right(), response_box.get_left(), color=PINK)

        self.play(Write(personalities))
        self.play(Create(config_box), Write(config_label))
        self.play(Create(response_box), Write(response_label))
        self.play(Create(arrow))

        # Show how personality affects responses
        example_responses = VGroup(
            Text("Deredere: 'I love you so much! 💕'", font_size=16, color=RED),
            Text("Tsundere: 'I-It's not like I like you! Baka!'", font_size=16, color=BLUE),
            Text("Kuudere: 'I see. That's interesting.'", font_size=16, color=GREEN),
        ).arrange(DOWN).move_to(DOWN * 2)

        self.play(Write(example_responses))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(personalities), FadeOut(config_box),
                  FadeOut(config_label), FadeOut(response_box), FadeOut(response_label),
                  FadeOut(arrow), FadeOut(example_responses))

    def explain_modes(self):
        title = Text("Conversation Modes", font_size=36, color=ORANGE)
        self.play(Write(title))

        # Mode types
        modes = VGroup(
            Text("Interactive Mode", font_size=24, color=GREEN),
            Text("Auto Mode", font_size=24, color=YELLOW),
            Text("Gemini Mode", font_size=24, color=PURPLE)
        ).arrange(DOWN, buff=0.8)

        # Mode descriptions
        descriptions = VGroup(
            Text("Real-time user interaction", font_size=16, color=GREEN_B),
            Text("AI vs AI conversation simulation", font_size=16, color=YELLOW_B),
            Text("Direct Gemini-powered responses", font_size=16, color=PURPLE_B)
        ).arrange(DOWN, buff=0.8)

        for mode, desc in zip(modes, descriptions):
            desc.next_to(mode, DOWN, buff=0.3)

        mode_group = VGroup(modes, descriptions).move_to(UP * 1)

        # Flow diagram
        user_box = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.2)
        user_label = Text("User", font_size=16).move_to(user_box.get_center())

        chatbot_box = Rectangle(width=2, height=1, color=RED, fill_opacity=0.2)
        chatbot_label = Text("Chatbot", font_size=16).move_to(chatbot_box.get_center())

        user_box.move_to(LEFT * 4 + DOWN * 2)
        chatbot_box.move_to(RIGHT * 4 + DOWN * 2)

        arrows = VGroup(
            Arrow(user_box.get_right(), chatbot_box.get_left(), color=GREEN),
            Arrow(chatbot_box.get_left(), user_box.get_right(), color=GREEN)
        )

        self.play(Write(mode_group))
        self.play(Create(user_box), Write(user_label))
        self.play(Create(chatbot_box), Write(chatbot_label))
        self.play(Create(arrows))

        # Show different mode behaviors
        mode_behaviors = VGroup(
            Text("Interactive: Human ↔ AI", font_size=18, color=GREEN),
            Text("Auto: AI ↔ AI (simulated)", font_size=18, color=YELLOW),
            Text("Gemini: Direct AI responses", font_size=18, color=PURPLE)
        ).arrange(DOWN).move_to(DOWN * 1.5)

        self.play(Write(mode_behaviors))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(mode_group), FadeOut(user_box),
                  FadeOut(user_label), FadeOut(chatbot_box), FadeOut(chatbot_label),
                  FadeOut(arrows), FadeOut(mode_behaviors))

    def explain_ai_integration(self):
        title = Text("AI Integration Layer", font_size=36, color=PURPLE)
        self.play(Write(title))

        # Gemini integration
        gemini_box = Rectangle(width=3, height=2, color=PURPLE, fill_opacity=0.2)
        gemini_label = Text("Google Gemini", font_size=20, color=PURPLE)
        gemini_label.move_to(gemini_box.get_center())
        gemini_label.move_to(LEFT * 4)

        # Prompt engineering
        prompt_box = Rectangle(width=3, height=2, color=BLUE, fill_opacity=0.2)
        prompt_label = Text("Prompt Engineering", font_size=16, color=BLUE)
        prompt_label.move_to(prompt_box.get_center())
        prompt_label.move_to(UP)

        # Response processing
        response_box = Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.2)
        response_label = Text("Response Processing", font_size=16, color=GREEN)
        response_label.move_to(response_box.get_center())
        response_label.move_to(RIGHT * 4)

        gemini_box.move_to(LEFT * 4)
        prompt_box.move_to(ORIGIN)
        response_box.move_to(RIGHT * 4)

        arrows = VGroup(
            Arrow(prompt_box.get_left(), gemini_box.get_right(), color=BLUE),
            Arrow(gemini_box.get_right(), response_box.get_left(), color=PURPLE)
        )

        # Features
        features = VGroup(
            Text("• Retry logic with exponential backoff", font_size=16, color=YELLOW),
            Text("• Echo detection and prevention", font_size=16, color=YELLOW),
            Text("• UTF-8 encoding support", font_size=16, color=YELLOW),
            Text("• Error handling and fallbacks", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(DOWN * 2)

        self.play(Create(gemini_box), Write(gemini_label))
        self.play(Create(prompt_box), Write(prompt_label))
        self.play(Create(response_box), Write(response_label))
        self.play(Create(arrows))
        self.play(Write(features))

        # Show prompt example
        prompt_example = Text('"You are a deredere waifu. Respond with love and enthusiasm!"',
                             font_size=14, color=BLUE_B).move_to(DOWN * 1.5)
        self.play(Write(prompt_example))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(gemini_box), FadeOut(gemini_label),
                  FadeOut(prompt_box), FadeOut(prompt_label), FadeOut(response_box),
                  FadeOut(response_label), FadeOut(arrows), FadeOut(features),
                  FadeOut(prompt_example))

    def explain_provider_system(self):
        title = Text("Provider Abstraction", font_size=36, color=RED)
        self.play(Write(title))

        # Provider interface
        interface_box = Rectangle(width=4, height=2, color=RED, fill_opacity=0.2)
        interface_label = Text("Classifier Interface", font_size=20, color=RED)
        interface_label.move_to(interface_box.get_center())
        interface_label.move_to(UP * 2)

        # Concrete providers
        gemini_provider = Rectangle(width=2.5, height=1.5, color=PURPLE, fill_opacity=0.2)
        gemini_provider_label = Text("Gemini", font_size=14, color=PURPLE)
        gemini_provider_label.move_to(gemini_provider.get_center())
        gemini_provider_label.move_to(LEFT *3  + DOWN * 1)

        openrouter_provider = Rectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.2)
        openrouter_provider_label = Text("OpenRouter", font_size=14, color=BLUE)
        openrouter_provider_label.move_to(openrouter_provider.get_center())
        openrouter_provider_label.move_to(RIGHT * 3 + DOWN + 1)

        interface_box.move_to(UP * 2)
        gemini_provider.move_to(LEFT * 3 + DOWN * 1)
        openrouter_provider.move_to(RIGHT * 3 + DOWN * 1)

        arrows = VGroup(
            Arrow(interface_box.get_bottom(), gemini_provider.get_top(), color=PURPLE),
            Arrow(interface_box.get_bottom(), openrouter_provider.get_top(), color=BLUE)
        )

        # Benefits
        benefits = VGroup(
            Text("• Easy provider switching", font_size=16, color=GREEN),
            Text("• Consistent API", font_size=16, color=GREEN),
            Text("• Extensible design", font_size=16, color=GREEN),
            Text("• Fallback support", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(DOWN * 2)

        self.play(Create(interface_box), Write(interface_label))
        self.play(Create(gemini_provider), Write(gemini_provider_label))
        self.play(Create(openrouter_provider), Write(openrouter_provider_label))
        self.play(Create(arrows))
        self.play(Write(benefits))

        # Show usage example
        usage_example = Text('classify("Hello!", provider="openrouter")', font_size=18, color=BLUE_B)
        usage_example.move_to(DOWN * 1)
        self.play(Write(usage_example))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(interface_box), FadeOut(interface_label),
                  FadeOut(gemini_provider), FadeOut(gemini_provider_label),
                  FadeOut(openrouter_provider), FadeOut(openrouter_provider_label),
                  FadeOut(arrows), FadeOut(benefits), FadeOut(usage_example))

    def show_data_flow(self):
        title = Text("Data Flow Architecture", font_size=36, color=YELLOW)
        self.play(Write(title))

        # Data flow components
        user_input = Text("User Input", font_size=20, color=BLUE)
        cli_parser = Text("CLI Parser", font_size=20, color=GREEN)
        mode_selection = Text("Mode Selection", font_size=20, color=YELLOW)
        ai_processing = Text("AI Processing", font_size=20, color=PURPLE)
        response_gen = Text("Response Generation", font_size=20, color=RED)
        output = Text("Console Output", font_size=20, color=ORANGE)

        components = VGroup(user_input, cli_parser, mode_selection, ai_processing, response_gen, output).arrange(DOWN, buff=0.8)

        # Create flow arrows
        arrows = VGroup()
        for i in range(len(components) - 1):
            arrow = Arrow(
                components[i].get_bottom(),
                components[i + 1].get_top(),
                color=YELLOW,
                stroke_width=3
            )
            arrows.add(arrow)

        # Position the flow
        components.move_to(UP)
        arrows.move_to(UP)

        # Data flow labels
        flow_labels = VGroup(
            Text("Command-line args", font_size=14, color=BLUE_B),
            Text("Configuration", font_size=14, color=GREEN_B),
            Text("Personality & Mode", font_size=14, color=YELLOW_B),
            Text("AI API calls", font_size=14, color=PURPLE_B),
            Text("Response formatting", font_size=14, color=RED_B),
            Text("User display", font_size=14, color=ORANGE)
        ).arrange(DOWN, buff=0.8)

        for label, component in zip(flow_labels, components):
            label.next_to(component, RIGHT)

        self.play(Write(components))
        self.play(Create(arrows))
        self.play(Write(flow_labels))

        # Show data transformation
        data_transformation = Text("Data transforms: Input → Config → AI → Response → Output",
                                  font_size=18, color=YELLOW).move_to(DOWN * 2.5)
        self.play(Write(data_transformation))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(components), FadeOut(arrows),
                  FadeOut(flow_labels), FadeOut(data_transformation))

    def show_conclusion(self):
        title = Text("Waifu Chatbot: Key Benefits", font_size=36, color=GREEN)
        title.move_to(UP*3)
        self.play(Write(title))

        # Key benefits
        benefits = VGroup(
            Text("🔧 Modular Architecture", font_size=24, color=BLUE),
            Text("🎭 Flexible Personality System", font_size=24, color=PINK),
            Text("🤖 Multiple AI Provider Support", font_size=24, color=PURPLE),
            Text("🚀 Easy to Extend and Maintain", font_size=24, color=GREEN),
            Text("⚡ Production-Ready Features", font_size=24, color=YELLOW)
        ).arrange(DOWN, buff=0.6)

        # Implementation details
        details = VGroup(
            Text("• Clean separation of concerns", font_size=16, color=BLUE),
            Text("• Comprehensive test coverage", font_size=16, color=PINK),
            Text("• Provider abstraction pattern", font_size=16, color=PURPLE),
            Text("• Error handling and logging", font_size=16, color=GREEN),
            Text("• Configuration management", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 2)

        self.play(Write(benefits))
        self.play(Write(details))
        self.wait(3)

        # Final message
        final_message = Text(
            "A sophisticated chatbot system demonstrating\n"
            "software architecture best practices!",
            font_size=28,
            color=GOLD
        ).move_to(DOWN * 3)

        self.play(Write(final_message))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(benefits), FadeOut(details), FadeOut(final_message))