import gradio as gr
import os
from pathlib import Path
from multi_agent import manager_agent
import base64

def chat_with_agent(message, history):
    """
    Simple chat function that runs the user's query through the multi-agent system
    """
    if not message.strip():
        return history, ""
    
    # Add user message to history
    history = history + [[message, None]]
    
    try:
        # Show progress in the chat
        history[-1][1] = "🚀 Starting analysis..."
        yield history, ""
        
        history[-1][1] = "🔍 Searching the web for information..."
        yield history, ""
        
        history[-1][1] = "🧠 Analyzing data and generating insights..."
        yield history, ""
        
        # Run the user's query directly through the manager agent
        result = manager_agent.run(message)
        
        history[-1][1] = "📊 Creating visualizations..."
        yield history, ""
        
        # Check if any image files were created
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.pdf']:
            image_files.extend(Path('.').glob(ext))
        
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
                final_response += f"\n\n📊 I've created a visualization saved as: {latest_image.name}"
        
        # Update with final result
        history[-1][1] = final_response
        yield history, ""
        
    except Exception as e:
        history[-1][1] = f"❌ Error occurred: {str(e)}"
        yield history, ""

def get_latest_image():
    """Get the most recently created image file"""
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.pdf']:
        image_files.extend(Path('.').glob(ext))
    
    if image_files:
        return str(max(image_files, key=os.path.getctime))
    return None

# Create simple interface
with gr.Blocks(title="Multi-Agent Research Assistant") as demo:
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>🤖 Multi-Agent Research & Visualization Assistant</h1>
        <p>Ask me anything! I can search the web, analyze data, and create visualizations for you.</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            # Chat interface with HTML support for inline images
            chatbot = gr.Chatbot(
                label="Chat",
                height=600,
                type="tuples",
                show_copy_button=True,
                elem_classes=["chat-container"]
            )
            
            msg = gr.Textbox(
                label="Message",
                placeholder="Ask me to research something and create a visualization...",
                lines=2,
                scale=4
            )
            
            with gr.Row():
                submit_btn = gr.Button("Send 📤", variant="primary", scale=1)
                clear_btn = gr.Button("Clear 🗑️", scale=1)
        
        with gr.Column(scale=1):
            # Status and backup image display
            gr.HTML("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <h4>📊 Latest Visualization</h4>
                <p style="font-size: 12px; color: #666;">Images also appear inline in the chat</p>
            </div>
            """)
            
            image_display = gr.Image(
                label="Backup Image View",
                show_download_button=True,
                height=300,
                show_label=False
            )
            
            refresh_img_btn = gr.Button("🔄 Refresh Image", size="sm")
    
    # Example buttons
    gr.HTML("<h3>💡 Try these examples:</h3>")
    with gr.Row():
        ex1 = gr.Button("🔋 LLM Training Power", size="sm")
        ex2 = gr.Button("⚡ Bitcoin vs AI Energy", size="sm")
        ex3 = gr.Button("🌱 Renewable Energy Growth", size="sm")

    def submit_and_refresh(message, history):
        """Submit message and refresh image"""
        # Process the chat
        for updated_history, _ in chat_with_agent(message, history):
            yield updated_history, "", get_latest_image()
    
    def clear_chat():
        return [], ""
    
    def refresh_image():
        return get_latest_image()
    
    # Event handlers
    submit_btn.click(
        submit_and_refresh,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, image_display]
    )
    
    msg.submit(
        submit_and_refresh,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, image_display]
    )
    
    clear_btn.click(
        clear_chat,
        outputs=[chatbot, msg]
    )
    
    refresh_img_btn.click(
        refresh_image,
        outputs=[image_display]
    )
    
    # Example button events
    ex1.click(lambda: "What is the current power consumption of LLM training?", outputs=msg)
    ex2.click(lambda: "Compare Bitcoin mining energy vs AI training energy consumption", outputs=msg)
    ex3.click(lambda: "Create a chart showing renewable energy growth by country", outputs=msg)

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
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 