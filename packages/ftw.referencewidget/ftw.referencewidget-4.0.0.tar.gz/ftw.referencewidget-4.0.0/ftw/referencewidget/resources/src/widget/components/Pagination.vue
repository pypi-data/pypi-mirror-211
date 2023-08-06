<template>
  <nav aria-label="Pagination for this listing" v-if="batching">
    <ul class="pagination">
      <li :class="batching.prev ? 'page-item' : 'page-item disabled'">
        <a href="#" @click.prevent="triggerPrevious" class="page-link">
          {{ $i18n("Previous") }}
        </a>
      </li>
      <li :class="batching.next ? 'page-item' : 'page-item disabled'">
        <a href="#" @click.prevent="triggerNext" class="page-link">
          {{ $i18n("Next") }}
        </a>
      </li>
    </ul>
  </nav>
</template>
<script>
export default {
  props: {
    batching: {
      type: Object,
      required: true,
      default: () => {
        return null;
      },
    },
  },
  methods: {
    triggerNext() {
      this.$emit("next", this.batching.next);
    },
    triggerPrevious() {
      this.$emit("previous", this.batching.prev);
    },
  },
};
</script>
