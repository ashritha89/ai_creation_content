import os
import streamlit as st
from dotenv import load_dotenv

from app.database import init_db, UserDB, HistoryDB
from app.auth import AuthManager
from app.content import ContentGenerator, ContentEvaluator, ContentRepurposer
from app.utils import is_valid_instruction, generate_title, create_download_link

st.set_page_config(
    page_title="AI Content Creator SaaS",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in environment variables")
    st.stop()

if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

content_generator = ContentGenerator(OPENAI_API_KEY)
content_evaluator = ContentEvaluator(OPENAI_API_KEY)
content_repurposer = ContentRepurposer(OPENAI_API_KEY)

if "user" not in st.session_state:
    st.session_state.user = None

if "show_auth" not in st.session_state:
    st.session_state.show_auth = False

if "pending_output" not in st.session_state:
    st.session_state.pending_output = None

if "pending_meta" not in st.session_state:
    st.session_state.pending_meta = None

def is_authenticated() -> bool:
    return st.session_state.user is not None

def require_auth():
    if not is_authenticated():
        st.session_state.show_auth = True
        st.rerun()

def render_auth_page():
    st.markdown("## 🔐 Authentication Required")
    st.markdown("Login or sign up to access full features.")
    
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔒 Password", type="password", key="login_pwd")
        
        if st.button("🚀 Login", key="login_btn", type="primary", use_container_width=True):
            if not email or not password:
                st.error("⚠️ Please enter both email and password")
            else:
                success, error_msg, user_data = AuthManager.login_user(email, password)
                if success:
                    st.session_state.user = user_data
                    st.session_state.show_auth = False
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {error_msg}")
    
    with tab2:
        st.markdown("### Create New Account")
        new_email = st.text_input("📧 Email", key="signup_email")
        new_password = st.text_input("🔒 Password", type="password", key="signup_pwd")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm")
        
        if st.button("📝 Sign Up", key="signup_btn", type="primary", use_container_width=True):
            if not new_email or not new_password:
                st.error("⚠️ Please fill in all fields")
            elif new_password != confirm_password:
                st.error("⚠️ Passwords do not match")
            else:
                success, error_msg, user_id = AuthManager.register_user(new_email, new_password)
                if success:
                    st.success("✅ Account created successfully! Please login.")
                    st.session_state.login_email = new_email
                else:
                    st.error(f"❌ {error_msg}")

def render_header():
    col1, col2 = st.columns([8, 2])
    
    with col1:
        st.markdown("# ✨ AI Content Creator SaaS")
        if is_authenticated():
            st.caption(f"Welcome back, {st.session_state.user['email']}! 🎉")
        else:
            st.caption("🔓 Free preview available • 🔐 Login for full access")
    
    with col2:
        if is_authenticated():
            with st.popover("👤 Account", use_container_width=True):
                st.markdown(f"**📧 {st.session_state.user['email']}**")
                st.markdown(f"**🆔 User ID:** {st.session_state.user['id']}")
                st.divider()
                if st.button("🚪 Logout", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.pending_output = None
                    st.session_state.pending_meta = None
                    st.session_state.show_auth = False
                    st.rerun()
        else:
            if st.button("🔐 Login / Sign Up", use_container_width=True, type="primary"):
                st.session_state.show_auth = True
                st.rerun()
    
    st.markdown("---")

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎛️ Content Settings")
        
        mode = st.radio(
            "🧠 Generation Mode",
            ["Direct Content", "Idea to Structured Content"],
            help="Direct: Generate immediately. Idea: Clarify idea first, then generate."
        )
        
        content_type = st.selectbox(
            "📄 Content Type",
            ["LinkedIn Post", "Professional Email", "Blog Paragraph", "Ad Copy"]
        )
        
        tone = st.selectbox(
            "🎭 Tone",
            ["Professional", "Friendly", "Formal", "Casual", "Motivational"]
        )
        
        audience = st.text_input(
            "🎯 Target Audience",
            value="Working professionals",
            help="Describe your target audience"
        )
        
        length = st.selectbox(
            "📏 Length",
            ["Short", "Medium", "Long"]
        )
        
        user_style = st.text_area(
            "🧬 Writing Style",
            placeholder="Optional: Describe your preferred writing style",
            help="E.g., 'Concise, data-driven, with examples'"
        )
        
        extra_notes = st.text_area(
            "📝 Extra Notes",
            placeholder="Optional: Additional requirements or context",
            help="Any specific requirements or context for the content"
        )
        
        repurpose = st.checkbox(
            "♻️ Repurpose Content",
            help="Generate LinkedIn, Email, and Ad Copy versions"
        )
        
        st.session_state.settings = {
            'mode': mode,
            'content_type': content_type,
            'tone': tone,
            'audience': audience,
            'length': length,
            'user_style': user_style,
            'extra_notes': extra_notes,
            'repurpose': repurpose
        }
        
        if is_authenticated():
            st.markdown("---")
            st.markdown("### 🕘 Content History")
            
            history = HistoryDB.get_user_history(st.session_state.user['id'], limit=20)
            
            if not history:
                st.info("No content history yet. Generate some content to see it here!")
            else:
                for item in history:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            if st.button(
                                f"📝 {item['title'][:30]}...",
                                key=f"view_{item['id']}",
                                use_container_width=True
                            ):
                                st.session_state.viewing_content = item
                                st.rerun()
                        with col2:
                            if st.button("🗑️", key=f"delete_{item['id']}"):
                                if HistoryDB.delete_content(st.session_state.user['id'], item['id']):
                                    st.success("✅ Deleted")
                                    st.rerun()
                        st.caption(f"📅 {item['timestamp']}")

def render_main_content():
    st.markdown("### ✍️ Content Generation")
    
    instruction = st.text_area(
        "What do you want to create?",
        height=150,
        placeholder="E.g., 'Write a LinkedIn post about the benefits of remote work for tech companies'",
        help="Enter your content idea or instruction here"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        generate_btn = st.button(
            "✨ Generate Content",
            type="primary",
            use_container_width=True
        )
    with col2:
        if is_authenticated() and st.session_state.pending_output:
            if st.button("🔄 Generate New", use_container_width=True):
                st.session_state.pending_output = None
                st.session_state.pending_meta = None
                st.rerun()
    
    if generate_btn:
        if not is_valid_instruction(instruction):
            st.warning("⚠️ Please enter a meaningful instruction (at least 3 words)")
        else:
            if 'settings' not in st.session_state:
                st.error("⚠️ Please configure settings in the sidebar first")
                st.stop()
            settings = st.session_state.settings
            
            with st.spinner("⏳ Generating content..."):
                try:
                    prompt = content_generator.build_prompt(
                        instruction,
                        settings['content_type'],
                        settings['tone'],
                        settings['audience'],
                        settings['length'],
                        settings['extra_notes'],
                        settings['user_style'],
                        settings['mode']
                    )
                    
                    full_output = content_generator.generate_content(prompt)
                    
                    st.session_state.pending_output = full_output
                    st.session_state.pending_meta = {
                        'instruction': instruction,
                        'content_type': settings['content_type'],
                        'tone': settings['tone'],
                        'prompt': prompt
                    }
                    
                    if not is_authenticated():
                        preview_lines = full_output.split('\n')[:3]
                        preview = '\n'.join(preview_lines)
                        if len(full_output.split('\n')) > 3:
                            preview += "\n..."
                        
                        st.markdown("### 👀 Preview (Limited)")
                        st.info(preview)
                        st.warning("🔒 **Login required** to view full content, download, quality score, and repurposing features.")
                        st.session_state.show_auth = True
                    else:
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Generation failed: {str(e)}")
    
    if is_authenticated() and st.session_state.pending_output:
        st.markdown("---")
        st.markdown("### ✅ Generated Content")
        
        st.text_area(
            "Full Content",
            value=st.session_state.pending_output,
            height=300,
            key="display_content",
            label_visibility="collapsed"
        )
        
        meta = st.session_state.pending_meta
        filename = f"{meta['content_type'].replace(' ', '_')}_{generate_title(meta['instruction']).replace(' ', '_')}.txt"
        create_download_link(st.session_state.pending_output, filename)
        
        title = generate_title(meta['instruction'])
        HistoryDB.save_content(
            user_id=st.session_state.user['id'],
            title=title,
            prompt=meta['instruction'],
            output=st.session_state.pending_output,
            content_type=meta['content_type'],
            tone=meta['tone']
        )
        st.success("✅ Content saved to history")
        
        st.markdown("### 📊 Quality Score")
        with st.spinner("Evaluating content quality..."):
            evaluation = content_evaluator.evaluate_content(
                st.session_state.pending_output,
                meta['content_type'],
                meta['tone']
            )
            st.success(evaluation)
        
        current_settings = st.session_state.get('settings', {})
        if current_settings.get('repurpose', False):
            st.markdown("### ♻️ Repurposed Content")
            with st.spinner("Repurposing content..."):
                repurposed = content_repurposer.repurpose_content(st.session_state.pending_output)
                st.info(repurposed)
        
        st.session_state.pending_output = None
        st.session_state.pending_meta = None

def render_history_view():
    if 'viewing_content' in st.session_state:
        item = st.session_state.viewing_content
        
        st.markdown("---")
        st.markdown(f"### 📝 {item['title']}")
        st.caption(f"📅 Created: {item['timestamp']}")
        
        st.markdown("**Original Prompt:**")
        st.info(item['prompt'])
        
        st.markdown("**Generated Content:**")
        st.text_area("", value=item['output'], height=300, key="history_content", label_visibility="collapsed")
        
        create_download_link(item['output'], f"{item['title'].replace(' ', '_')}.txt")
        
        if st.button("← Back to Main"):
            del st.session_state.viewing_content
            st.rerun()

def main():
    render_header()
    
    if st.session_state.show_auth and not is_authenticated():
        render_auth_page()
        return
    
    render_sidebar()
    
    if 'viewing_content' in st.session_state:
        render_history_view()
    else:
        render_main_content()

if __name__ == "__main__":
    main()
