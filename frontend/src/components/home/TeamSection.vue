<template>
  <section class="gc-team">
    <div class="gc-team-inner">
      <header class="gc-team-header">
        <h2 class="gc-team-title">
          {{ t('home.team.title') }}
          <span class="gc-gradient-text">{{ t('home.team.titleHighlight') }}</span>
        </h2>

        <div v-if="!loading && members.length > 0" class="gc-team-controls">
          <button
            type="button"
            class="gc-team-arrow"
            :disabled="!canPrev"
            aria-label="Previous"
            @click="scrollBy(-1)"
          >
            <q-icon name="arrow_back" size="20px" />
          </button>
          <button
            type="button"
            class="gc-team-arrow gc-team-arrow-primary"
            :disabled="!canNext"
            aria-label="Next"
            @click="scrollBy(1)"
          >
            <q-icon name="arrow_forward" size="20px" />
          </button>
        </div>
      </header>

      <div v-if="loading" class="gc-team-loading">
        <q-spinner color="primary" size="32px" />
      </div>

      <p v-else-if="members.length === 0" class="gc-team-empty">
        {{ t('home.team.empty') }}
      </p>

      <div v-else ref="scrollEl" class="gc-team-scroll">
        <article v-for="member in members" :key="member.id" class="gc-team-card">
          <div class="gc-team-photo-wrap">
            <img
              v-if="member.photo_url"
              :src="member.photo_url"
              :alt="member.name"
              class="gc-team-photo"
              loading="lazy"
            />
            <div v-else class="gc-team-photo-placeholder">
              <q-icon name="person" size="48px" />
            </div>
          </div>
          <div class="gc-team-text">
            <h3 class="gc-team-name">{{ member.name }}</h3>
            <p class="gc-team-role">
              <span class="gc-team-role-dot" aria-hidden="true"></span>
              {{ member.role }}
            </p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { teamService, type TeamMember } from 'src/services/team';

const { t, locale } = useI18n();

const members = ref<TeamMember[]>([]);
const loading = ref(true);
const scrollEl = ref<HTMLElement | null>(null);
const canPrev = ref(false);
const canNext = ref(false);

async function load() {
  loading.value = true;
  try {
    members.value = await teamService.list();
  } catch {
    members.value = [];
  } finally {
    loading.value = false;
  }
}

function updateScrollState() {
  const el = scrollEl.value;
  if (!el) return;
  canPrev.value = el.scrollLeft > 8;
  canNext.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 8;
}

function scrollBy(direction: -1 | 1) {
  const el = scrollEl.value;
  if (!el) return;
  const card = el.querySelector('.gc-team-card');
  const step = card ? card.offsetWidth + 24 : 320;
  el.scrollBy({ left: step * direction, behavior: 'smooth' });
}

onMounted(async () => {
  await load();
  await new Promise((r) => requestAnimationFrame(() => r(null)));
  updateScrollState();
  scrollEl.value?.addEventListener('scroll', updateScrollState, { passive: true });
  window.addEventListener('resize', updateScrollState);
});

watch(locale, load);
</script>

<style scoped lang="scss">
.gc-team {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px;
  }
}

.gc-team-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.gc-team-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.gc-team-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-team-controls {
  display: flex;
  gap: 8px;
}

.gc-team-arrow {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: var(--gc-bg-soft);
  color: var(--gc-text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease,
    opacity 0.15s ease;

  &:hover:not(:disabled) {
    background: var(--gc-border);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.gc-team-arrow-primary {
  background: var(--gc-primary);
  color: #ffffff;

  &:hover:not(:disabled) {
    background: var(--gc-primary);
    filter: brightness(1.08);
  }
}

.gc-team-loading {
  display: flex;
  justify-content: center;
  padding: 48px 0;
}

.gc-team-empty {
  color: var(--gc-text-muted);
  text-align: center;
  margin: 0;
  padding: 48px 0;
}

.gc-team-scroll {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 75%;
  gap: 16px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding-bottom: 4px;

  &::-webkit-scrollbar {
    display: none;
  }

  @media (min-width: 600px) {
    grid-auto-columns: 45%;
    gap: 24px;
  }

  @media (min-width: 900px) {
    grid-auto-columns: 30%;
  }

  @media (min-width: 1100px) {
    grid-auto-columns: minmax(0, 1fr);
    grid-template-columns: repeat(4, 1fr);
    overflow-x: visible;
  }
}

.gc-team-card {
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-team-photo-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: var(--gc-radius-lg);
  overflow: hidden;
  background: var(--gc-bg-soft);
}

.gc-team-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.gc-team-photo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gc-text-muted);
}

.gc-team-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gc-team-name {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-team-role {
  font-size: 12px;
  color: var(--gc-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.gc-team-role-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.6;
}
</style>
