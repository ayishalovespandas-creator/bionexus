import streamlit as st
from PIL import Image

from filter_analyzer import analyze_filter
from tank_analyzer import analyze_tank

st.set_page_config(
    page_title="bionexus AI",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 bionexus AI")
st.subheader("Bladderwort-Inspired Microplastic Monitoring System")

st.info(
    "AI-assisted prototype for estimating visible particles, "
    "filter condition and device performance."
)

st.header("📸 1. Filter Analysis")

filter_photo = st.file_uploader(
    "Upload a photo of the used filter",
    type=["jpg", "jpeg", "png"],
    key="filter"
)

filter_particles = None
filter_loading = None

if filter_photo:
    filter_image = Image.open(filter_photo)

    st.image(
        filter_image,
        caption="Uploaded Filter",
        width=500
    )

    if st.button("Analyze Filter"):
        result, filter_particles, filter_loading = analyze_filter(
            filter_image
        )

        st.image(
            result,
            caption="AI Particle Detection"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Estimated Particles",
                filter_particles
            )

        with col2:
            st.metric(
                "Filter Loading",
                f"{filter_loading}%"
            )

st.header("⏱️ 2. Machine Usage")

hours = st.number_input(
    "How many hours has the machine operated?",
    min_value=0.0,
    max_value=1000.0,
    value=1.0,
    step=0.5
)

if filter_loading is not None:

    st.header("🔧 Filter Condition")

    if filter_loading < 40:
        status = "🟢 FILTER OK"

    elif filter_loading < 70:
        status = "🟡 MONITOR FILTER"

    elif filter_loading < 85:
        status = "🟠 REPLACE SOON"

    else:
        status = "🔴 REPLACE FILTER"

    st.subheader(status)

    st.write(
        f"Machine operating time: **{hours:.1f} hours**"
    )

st.header("📸 3. Tank Analysis")

before_photo = st.file_uploader(
    "Upload BEFORE tank photo",
    type=["jpg", "jpeg", "png"],
    key="before"
)

after_photo = st.file_uploader(
    "Upload AFTER tank photo",
    type=["jpg", "jpeg", "png"],
    key="after"
)

if before_photo and after_photo:

    before_image = Image.open(before_photo)
    after_image = Image.open(after_photo)

    if st.button("Analyze Tank"):

        before_result, before_count = analyze_tank(
            before_image
        )

        after_result, after_count = analyze_tank(
            after_image
        )

        st.image(
            before_result,
            caption="Before Filtration"
        )

        st.image(
            after_result,
            caption="After Filtration"
        )

        if before_count > 0:

            performance = (
                (before_count - after_count)
                / before_count
            ) * 100

            performance = max(
                0,
                min(100, performance)
            )

            st.header("🌊 Device Performance")

            st.metric(
                "Estimated Particle Reduction",
                f"{performance:.1f}%"
            )

            if performance >= 80:
                st.success(
                    "High estimated particle reduction"
                )

            elif performance >= 50:
                st.warning(
                    "Moderate estimated particle reduction"
                )

            else:
                st.error(
                    "Low estimated particle reduction"
                )

st.divider()

st.caption(
    "⚠️ AI-assisted visual estimate. "
    "A photograph cannot chemically confirm that detected particles "
    "are microplastics."
)
