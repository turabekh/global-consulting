<template>
  <q-page class="gc-home">
    <HeroSection />
    <AboutStatsSection />
    <ServicesPreviewSection />
    <TeamSection />
    <TestimonialsSection />
    <FaqSection />
    <ContactCtaSection />
    <BlogPreviewSection />
  </q-page>
</template>

<script setup lang="ts">
import HeroSection from 'src/components/home/HeroSection.vue';
import AboutStatsSection from 'src/components/home/AboutStatsSection.vue';
import ServicesPreviewSection from 'src/components/home/ServicesPreviewSection.vue';
import TeamSection from 'src/components/home/TeamSection.vue';
import TestimonialsSection from 'src/components/home/TestimonialsSection.vue';
import FaqSection from 'src/components/home/FaqSection.vue';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';
import BlogPreviewSection from 'src/components/home/BlogPreviewSection.vue';
</script>

<style scoped lang="scss">
.gc-home {
  background: var(--gc-bg);
}
</style>
