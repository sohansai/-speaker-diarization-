import spaces 
from app.ui.interface import create_gradio_interface 

if __name__ == "__main__":
    demo = create_gradio_interface()  # Create interface
    demo.launch(share=True)  # Launch interface
