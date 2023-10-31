<script lang="ts">
  export let data: any[];

  const width = [null, 1, 2, 3, 4, 5].map(
    (e) => (data.filter((f) => f === e).length / data.length) * 100
  );

  const widthr = width.map((e) => parseFloat(e.toFixed(0)));
</script>

<div style="width: 100%; height: 20px; position: relative;">
  <div style="width: 100%; height: 20px; position: relative;">
    <div
      style="background-color: #708090; width: {width[0]}%; height: 100%; position: absolute;"
      data-tooltip="N/A: {widthr[0]}%"
    />
    <div
      style="background-color: #FF0000; width: {width[1]}%; height: 100%; position: absolute; left: {width[0]}%"
      data-tooltip="1 star: {widthr[1]}%"
    />
    <div
      style="background-color: #FF5500; width: {width[2]}%; height: 100%; position: absolute; left: {width[0] +
        width[1]}%;"
      data-tooltip="2 star: {widthr[2]}%"
    />
    <div
      style="background-color: #FFAA00; width: {width[3]}%; height: 100%; position: absolute; left: {width[0] +
        width[1] +
        width[2]}%;"
      data-tooltip="3 star: {widthr[3]}%"
    />
    <div
      style="background-color: #AAFF00; width: {width[4]}%; height: 100%; position: absolute; left: {width[0] +
        width[1] +
        width[2] +
        width[3]}%;"
      data-tooltip="4 star: {widthr[4]}%"
    />
    <div
      style="background-color: #00FF00; width: {width[5]}%; height: 100%; position: absolute; left: {width[0] +
        width[1] +
        width[2] +
        width[3] +
        width[4]}%;"
      data-tooltip="5 star: {widthr[5]}%"
    />
  </div>
</div>

<style>
  [data-tooltip] {
    position: relative;
    z-index: 2;
    display: block;
  }

  [data-tooltip]:before,
  [data-tooltip]:after {
    visibility: hidden;
    opacity: 0;
    pointer-events: none;
    transition: 0.2s ease-out;
    transform: translate(-50%, 5px);
  }

  [data-tooltip]:before {
    position: absolute;
    bottom: 100%;
    left: 50%;
    margin-bottom: 5px;
    padding: 7px;
    width: 100%;
    min-width: 70px;
    max-width: 250px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
    background-color: #000;
    background-color: hsla(0, 0%, 20%);
    color: #fff;
    content: attr(data-tooltip);
    text-align: center;
    font-size: 14px;
    line-height: 1.2;
    transition: 0.2s ease-out;
  }

  [data-tooltip]:after {
    position: absolute;
    bottom: 100%;
    left: 50%;
    width: 0;
    border-top: 5px solid #000;
    border-top: 5px solid hsla(0, 0%, 20%, 0.9);
    border-right: 5px solid transparent;
    border-left: 5px solid transparent;
    content: " ";
    font-size: 0;
    line-height: 0;
  }

  [data-tooltip]:hover:before,
  [data-tooltip]:hover:after {
    visibility: visible;
    opacity: 1;
    transform: translate(-50%, 0);
  }
</style>
