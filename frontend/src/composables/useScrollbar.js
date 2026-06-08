import { ref, onMounted} from 'vue';

export function useScrollbar() {
  const scrollbar = ref(null);
  const scrollbarContainer = ref(null);
  const scrollContainer = ref(null);

  const setup = () => {
    if (!scrollContainer.value || !scrollbar.value || !scrollbarContainer.value) return;

    const updateScrollbar = () => {
      const container = scrollContainer.value;
      const scrollbarEl = scrollbar.value;
      const containerEl = scrollbarContainer.value;

      if (container.scrollWidth > container.clientWidth) {
        const scrollRatio = container.scrollLeft / (container.scrollWidth - container.clientWidth);
        const scrollbarWidth = containerEl.clientWidth * (container.clientWidth / container.scrollWidth);
        
        scrollbarEl.style.width = `${Math.max(30, scrollbarWidth)}px`;
        scrollbarEl.style.left = `${scrollRatio * (containerEl.clientWidth - scrollbarWidth)}px`;
        containerEl.style.display = 'block';
      } else {
        containerEl.style.display = 'none';
      }
    };

    const handleScroll = () => {
      updateScrollbar();
    };

    // Make scrollbar draggable
    let isDragging = false;
    let startX, startLeft;

    const onMouseDown = (e) => {
      isDragging = true;
      startX = e.clientX;
      startLeft = scrollbar.value.offsetLeft;
      document.body.style.cursor = 'grabbing';
      e.preventDefault();
    };

    const onMouseMove = (e) => {
      if (!isDragging) return;
      
      const containerWidth = scrollbarContainer.value.clientWidth;
      const scrollbarWidth = scrollbar.value.clientWidth;
      const maxLeft = containerWidth - scrollbarWidth;
      const newLeft = startLeft + (e.clientX - startX);
      const clampedLeft = Math.max(0, Math.min(maxLeft, newLeft));
      
      scrollbar.value.style.left = `${clampedLeft}px`;
      
      const scrollRatio = clampedLeft / maxLeft;
      scrollContainer.value.scrollLeft = scrollRatio * 
        (scrollContainer.value.scrollWidth - scrollContainer.value.clientWidth);
    };

    const onMouseUp = () => {
      isDragging = false;
      document.body.style.cursor = '';
    };

    // Set up event listeners
    scrollContainer.value.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', updateScrollbar);
    scrollbar.value.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);

    // Initial update
    updateScrollbar();

    // Cleanup function
    return () => {
      scrollContainer.value?.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', updateScrollbar);
      scrollbar.value?.removeEventListener('mousedown', onMouseDown);
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };
  };

  onMounted(() => {
    setup();
  });

  return {
    scrollbar,
    scrollbarContainer,
    scrollContainer
  };
}
