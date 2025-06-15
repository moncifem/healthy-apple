import gradio as gr
import os
from pathlib import Path
from multi_agent import create_main_agent
from smolagents import MCPClient
from sql_agent import SERVER_PARAMETERS
import base64

RESPONSE_INSTRUCTIONS = {
    "Short Answer": "Provide a short, concise answer to the user's question.",
    "Detailed Report": """
1. Use the sql_query_agent_health managed agent to get a detailed view of the user's health data.
2. Use the web search managed agent to include benchmark comparisons to the general population and other relevant data.
3. Use the visual_agent to create a visualization to help the user understand the data.
""",
}


def chat_with_agent(message, history, response_mode):
    """
    Simple chat function that runs the user's query through the multi-agent system
    """
    if not message.strip():
        return history, ""

    # Add user message to history
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": None},
    ]

    try:
        # Step 1: Starting analysis with animation
        history[-1]["content"] = """
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 16px; margin: 1rem 0;">
            <div style="display: inline-block; position: relative;">
                <div style="font-size: 4rem; animation: bounce 1s ease-in-out infinite;">🚀</div>
                <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); width: 60px; height: 4px; background: #6366f1; border-radius: 2px; animation: pulse 1s ease-in-out infinite;"></div>
            </div>
            <h2 style="margin-top: 2rem; color: #1e293b;">Initializing Health Analysis</h2>
            <p style="color: #64748b;">Preparing to analyze your health data...</p>
        </div>
        <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            @keyframes pulse {
                0%, 100% { transform: translateX(-50%) scaleX(1); opacity: 1; }
                50% { transform: translateX(-50%) scaleX(1.5); opacity: 0.7; }
            }
        </style>
        """
        yield history, ""

        # Step 2: Searching database
        history[-1]["content"] = """
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 16px; margin: 1rem 0;">
            <div style="display: inline-block; position: relative;">
                <div style="font-size: 4rem; animation: bounce 1s ease-in-out infinite;">🔍</div>
                <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); width: 60px; height: 4px; background: #f59e0b; border-radius: 2px; animation: pulse 1s ease-in-out infinite;"></div>
            </div>
            <h2 style="margin-top: 2rem; color: #1e293b;">Searching Health Database</h2>
            <p style="color: #64748b;">Querying your health records and metrics...</p>
        </div>
        """
        yield history, ""

        # Step 3: Analyzing data
        history[-1]["content"] = """
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); border-radius: 16px; margin: 1rem 0;">
            <div style="display: inline-block; position: relative;">
                <div style="font-size: 4rem; animation: bounce 1s ease-in-out infinite;">🧠</div>
                <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); width: 60px; height: 4px; background: #8b5cf6; border-radius: 2px; animation: pulse 1s ease-in-out infinite;"></div>
            </div>
            <h2 style="margin-top: 2rem; color: #1e293b;">Analyzing Health Patterns</h2>
            <p style="color: #64748b;">Processing data and generating insights...</p>
        </div>
        """
        yield history, ""

        # Add mode instruction to the message
        modified_message = f"{message}\n\n{RESPONSE_INSTRUCTIONS[response_mode]}"

        # Debug: Print the modified message
        print(f"\n🔍 DEBUG - Modified message being sent to manager_agent:")
        print(f"{modified_message}\n")

        # Run the user's query directly through the manager agent
        try:
            result = demo.manager_agent.run(modified_message)
            print(f"\n✅ DEBUG - Manager agent returned result of type: {type(result)}")
            print(f"Result preview: {str(result)[:200]}...\n")
        except Exception as e:
            print(f"\n❌ DEBUG - Manager agent error: {str(e)}")
            raise

        # Step 4: Creating visualizations
        history[-1]["content"] = """
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 16px; margin: 1rem 0;">
            <div style="display: inline-block; position: relative;">
                <div style="font-size: 4rem; animation: bounce 1s ease-in-out infinite;">📊</div>
                <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); width: 60px; height: 4px; background: #10b981; border-radius: 2px; animation: pulse 1s ease-in-out infinite;"></div>
            </div>
            <h2 style="margin-top: 2rem; color: #1e293b;">Creating Visualizations</h2>
            <p style="color: #64748b;">Generating charts and visual insights...</p>
        </div>
        """
        yield history, ""

        # Check if any image files were created
        image_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg", "*.svg", "*.pdf"]:
            image_files.extend(Path(".").glob(ext))

        # Prepare final response with inline image
        final_response = result

        if image_files:
            latest_image = max(image_files, key=os.path.getctime)
            image_path = str(latest_image)

            # Create HTML img tag for inline display
            try:
                # Convert image to base64 for inline display
                with open(image_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                    img_html = f'<img src="data:image/png;base64,{img_data}" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;">'

                final_response += f"\n\n📊 I've created a visualization:\n\n{img_html}"
            except Exception as e:
                final_response += (
                    f"\n\n📊 I've created a visualization saved as: {latest_image.name}"
                )

        # Update with final result
        history[-1]["content"] = final_response
        yield history, ""

    except Exception as e:
        history[-1]["content"] = f"""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-radius: 16px; margin: 1rem 0;">
            <div style="display: inline-block; position: relative;">
                <div style="font-size: 4rem;">❌</div>
            </div>
            <h2 style="margin-top: 2rem; color: #dc2626;">Analysis Error</h2>
            <p style="color: #7f1d1d;">{str(e)}</p>
            <p style="color: #991b1b; margin-top: 1rem; font-size: 0.9rem;">Please try again or contact support if the issue persists.</p>
        </div>
        """
        yield history, ""


def get_latest_image():
    """Get the most recently created image file"""
    image_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.svg", "*.pdf"]:
        image_files.extend(Path(".").glob(ext))

    if image_files:
        return str(max(image_files, key=os.path.getctime))
    return None


# Create simple interface
with gr.Blocks(title="Apple Health Assistant") as demo:
    with MCPClient(SERVER_PARAMETERS) as mcp_client:
        manager_agent = create_main_agent(mcp_client)

        gr.HTML(
            """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>🍏 Health Assistant</h1>
            <p>Ask me anything about your health! I'll help you understand your health data and create a health improvement plan.</p>
        </div>
        """
        )

        with gr.Row():
            with gr.Column(scale=3):
                # Response mode selection
                response_mode = gr.Radio(
                    choices=["Short Answer", "Detailed Report"],
                    value="Short Answer",
                    label="Response Mode",
                    info="Choose how detailed you want the response to be",
                )

                # Chat interface with HTML support for inline images
                chatbot = gr.Chatbot(
                    label="Chat",
                    height=600,
                    type="messages",
                    show_copy_button=True,
                    elem_classes=["chat-container"],
                )

                msg = gr.Textbox(
                    label="Message",
                    placeholder="Ask me to research something and create a visualization...",
                    lines=2,
                    scale=4,
                )

                with gr.Row():
                    submit_btn = gr.Button("Send 📤", variant="primary", scale=1)
                    clear_btn = gr.Button("Clear 🗑️", scale=1)

            with gr.Column(scale=1):
                # Status and backup image display
                gr.HTML(
                    """
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <h4>📊 Latest Visualization</h4>
                    <p style="font-size: 12px; color: #666;">Images also appear inline in the chat</p>
                </div>
                """
                )

                image_display = gr.Image(
                    label="Backup Image View",
                    show_download_button=True,
                    height=300,
                    show_label=False,
                )

                refresh_img_btn = gr.Button("🔄 Refresh Image", size="sm")

        # Example buttons
        gr.HTML("<h3>💡 Try these examples:</h3>")
        with gr.Row():
            ex1 = gr.Button("💓 Heart Health", size="sm")
            ex2 = gr.Button("💤 Sleep Health", size="sm")
            ex3 = gr.Button("🏃 Activity Level", size="sm")

        def submit_and_refresh(message, history, response_mode):
            """Submit message and refresh image"""
            # Process the chat
            for updated_history, _ in chat_with_agent(message, history, response_mode):
                yield updated_history, "", get_latest_image()

        def clear_chat():
            return [], ""

        def refresh_image():
            return get_latest_image()

        # Store manager_agent as demo attribute for access in functions
        demo.manager_agent = manager_agent

        # Event handlers
        submit_btn.click(
            submit_and_refresh,
            inputs=[msg, chatbot, response_mode],
            outputs=[chatbot, msg, image_display],
        )

        msg.submit(
            submit_and_refresh,
            inputs=[msg, chatbot, response_mode],
            outputs=[chatbot, msg, image_display],
        )

        clear_btn.click(clear_chat, outputs=[chatbot, msg])

        refresh_img_btn.click(refresh_image, outputs=[image_display])

        # Example button events
        ex1.click(
            lambda: "How is my heart health, compared to people in my age group?", outputs=msg
        )
        ex2.click(lambda: "How well am I sleeping?", outputs=msg)
        ex3.click(lambda: "How can I improve my activity level?", outputs=msg)

        # Add custom CSS for better image display in chat
        demo.css = """
        .chat-container .message img {
            max-width: 100% !important;
            height: auto !important;
            border-radius: 8px !important;
            margin: 10px 0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        .chat-container {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        """

if __name__ == "__main__":
    # Ensure we have write permissions in current directory
    try:
        test_file = Path("test_write.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permissions confirmed")
    except Exception as e:
        print(f"⚠️  Warning: Write permission issue: {e}")

    # Check if API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please set your Anthropic API key to use this application.")

    print("🚀 Starting Multi-Agent Assistant...")
    print("💬 Chat interface with inline image display!")
    print("📊 Images will appear both in chat and in the side panel")

    # Launch the app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)
