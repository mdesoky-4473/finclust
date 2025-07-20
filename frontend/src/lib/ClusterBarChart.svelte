<script lang="ts">
  import { onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  export let data: Record<string, number>;

  let canvas: HTMLCanvasElement;
  let chart: Chart;

    $: if (canvas && data) {
    if (chart) chart.destroy();

    const sortedLabels = Object.keys(data).sort((a, b) => {
      const numA = parseInt(a.replace(/\D/g, ''));
      const numB = parseInt(b.replace(/\D/g, ''));
      return numA - numB;
    });

    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: sortedLabels,
        datasets: [{
          label: 'Users per Cluster',
          data: sortedLabels.map(label => data[label]),
          backgroundColor: sortedLabels.map((_, i) => {
            const colors = [
              'rgba(34, 197, 94, 0.9)',     // Green
              'rgba(99, 102, 241, 0.9)',    // Indigo
              'rgba(251, 191, 36, 0.9)',    // Amber
              'rgba(239, 68, 68, 0.9)',     // Red
              'rgba(59, 130, 246, 0.9)',    // Blue 
              'rgba(147, 51, 234, 0.9)'     // Purple
            ];
            return colors[i % colors.length];
          })
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        }
      }
    });
  }


  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<div class="w-full md:w-[600px] h-[400px]">
  <canvas bind:this={canvas}></canvas>
</div>

