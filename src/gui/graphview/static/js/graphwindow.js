$(function () {
    const MIN_WIDTH = 300
    const MIN_HEIGHT = 200
    const NODE_RADIUS = 20

    const ARROW_STATE = ['Normal', 'AddNode', 'AddEdge', 'Delete']
    let current_arrow_state = ARROW_STATE[0]

    let _nodes = new Map()
    let _edges = new Map()
    let node_count = 1

    let $window = $(window);
    let two = new Two({
        type: Two.Types.svg,
        autostart: true,
        width: MIN_WIDTH,
        height: MIN_HEIGHT
    }).appendTo($("#graph_view")[0]);
    let $svg = $(two.scene._renderer.elem)

    let border = two.makeRoundedRectangle(two.width / 2, two.height / 2, two.width - 2, two.height - 2, 2);
    border.linewidth = 1
    border.stroke = 'grey'

    let btnZoomIndicatingLine = two.makeLine(two.width - 13, two.height - 3, two.width - 3, two.height - 13)
    let btnZoomIndicatingLine2 = two.makeLine(two.width - 8, two.height - 3, two.width - 3, two.height - 8)
    btnZoomIndicatingLine.stroke = 'grey'
    btnZoomIndicatingLine2.stroke = 'grey'

    let btnZoom = two.makeRectangle(two.width - 8, two.height - 8, 15, 15)
    btnZoom.noStroke()
    btnZoom.fill = 'grey'
    btnZoom.opacity = 0.01

    two.update()

    function resize(pos, offsetX, offsetY) {
        two.width = pos.x + 8 + offsetX
        two.height = pos.y + 8 + offsetY
        if(two.width < MIN_WIDTH) two.width = MIN_WIDTH
        if(two.height < MIN_HEIGHT) two.height = MIN_HEIGHT
        border.width = two.width - 2
        border.height = two.height - 2
        border.position.set(two.width / 2, two.height / 2)
        btnZoomIndicatingLine.vertices[0].set(two.width - 13, two.height - 3)
        btnZoomIndicatingLine.vertices[1].set(two.width - 3, two.height - 13)
        btnZoomIndicatingLine2.vertices[0].set(two.width - 8, two.height - 3)
        btnZoomIndicatingLine2.vertices[1].set(two.width - 3, two.height - 8)
        btnZoom.position.set(two.width - 8, two.height - 8)
    }
    $(btnZoom._renderer.elem).css({ cursor: 'se-resize' })
    bindBtnMoveEvent(btnZoom, resize)

    let tmpEdge = null
    let tmpStartShape = null
    let tmpEndShape = null

    function addInteractivity(shape, text) {
        let svgP = $svg.offset()
        let pos = new Two.Vector(0, 0)
        let pressP = new Two.Vector(0, 0)
        function onMouseDown(e) {
            e.preventDefault();
            // 删除节点分支
            if(current_arrow_state === ARROW_STATE[3]) {
                delNode(shape)
                return false
            }
            pos.set(shape.position.x, shape.position.y)
            pressP.set(e.clientX, e.clientY)
            $window
                .bind('mousemove', onMouseMove)
                .bind('mouseup', onMouseUp);
            // 添加边分支，绘制临时指示线
            if(current_arrow_state === ARROW_STATE[2]) {
                tmpStartShape = shape
                tmpEdge = two.makeLine(shape.position.x, shape.position.y, shape.position.x, shape.position.y)
                tmpEdge.linewidth = 4
                tmpEdge.opacity = 0.75
                tmpEdge.stroke = 'grey'

                shape.fill = 'rgb(252,185,69)'
            }
            return false
        }
        function onMouseMove(e) {
            e.preventDefault();
            // 节点正常拖拽分支
            if(current_arrow_state !== ARROW_STATE[2]) {
                let offsetX = e.clientX - pressP.x;
                let offsetY = e.clientY - pressP.y;
                shape.position.set(pos.x + offsetX, pos.y + offsetY)
                onNodeMove(shape)
            }
            // 添加边分支，节点不动，绘制临时指示线
            else if(current_arrow_state === ARROW_STATE[2]) {
                if(!tmpEndShape)
                    tmpEdge.vertices[1].set(e.clientX - svgP.left, e.clientY - svgP.top)
                else {
                    let tmpEnd = cutout(tmpStartShape.position, tmpEndShape.position, NODE_RADIUS)
                    tmpEdge.vertices[1].set(tmpEnd.x, tmpEnd.y)
                }
            }
        }
        function onMouseUp(e) {
            e.preventDefault();
            $window
                .unbind('mousemove', onMouseMove)
                .unbind('mouseup', onMouseUp);
            if(tmpEdge)
                two.remove(tmpEdge)

            if(tmpEndShape) {
                addEdge(tmpStartShape, tmpEndShape)
                tmpEndShape.fill = 'rgb(0,200,255)'
            }
            if(tmpStartShape)
                tmpStartShape.fill = 'rgb(0,200,255)'
            tmpStartShape = null
            tmpEndShape = null
        }
        function onMouseEnter(e) {
            e.preventDefault();
            if(current_arrow_state === ARROW_STATE[3])
                shape.stroke = 'red'
            else
                shape.stroke = 'green'

            if(current_arrow_state === ARROW_STATE[2]) {
                if(tmpStartShape && tmpStartShape !== shape) {
                    shape.fill = 'rgb(252,185,69)'
                    tmpEndShape = shape
                }
            }
        }
        function onMouseLeave(e) {
            e.preventDefault();
            shape.stroke = 'grey'

            if(tmpStartShape !== shape) {
                shape.fill = 'rgb(0,200,255)'
                tmpEndShape = null
            }
        }
        $(shape._renderer.elem)
            .bind('mousedown', onMouseDown)
            .bind('mouseenter', onMouseEnter)
            .bind('mouseleave', onMouseLeave)

        $(text._renderer.elem)
            .bind('mousedown', function (e) { e.preventDefault(); return onMouseDown(e); })
            .bind('mouseenter', function (e) { e.preventDefault(); return onMouseEnter(e); })
            .bind('mouseleave', function (e) { e.preventDefault(); return onMouseLeave(e); })
    }

    function bindBtnMoveEvent(shape, handleFunc) {
        let pos = new Two.Vector(0, 0)
        let pressP = new Two.Vector(0, 0)
        function onMouseDown(e) {
            e.preventDefault();
            pos.set(shape.position.x, shape.position.y)
            pressP.set(e.clientX, e.clientY)
            $window
                .bind('mousemove', onMouseMove)
                .bind('mouseup', onMouseUp);
            return false
        }
        function onMouseMove(e) {
            e.preventDefault();
            let offsetX = e.clientX - pressP.x;
            let offsetY = e.clientY - pressP.y;
            handleFunc(pos, offsetX, offsetY)
        }
        function onMouseUp(e) {
            e.preventDefault();
            $window
                .unbind('mousemove', onMouseMove)
                .unbind('mouseup', onMouseUp);
        }
        $(shape._renderer.elem).bind('mousedown', onMouseDown)
    }

    // 按钮样式
    let btnNormalCSS = {
        height: 23,
        cursor: 'pointer',
        border: '1px solid grey',
        borderRadius: 2,
        background: 'rgb(243, 243, 243)'
    }
    let btnSelectedCSS = Object.create(btnNormalCSS)
    btnSelectedCSS.background = 'rgb(198, 198, 198)'
    function setCSSBtnNormal(btnID) {
        $(btnID).css(btnNormalCSS)
    }
    function setCSSBtnSelected(btnID) {
        $(btnID).css(btnSelectedCSS)
    }

    setCSSBtnNormal('#btn_add_node')
    setCSSBtnNormal('#btn_add_edge')
    setCSSBtnNormal('#btn_delete')

    // 按钮事件
    function onBtnAddNodeClick(e) {
        setCSSAllNormal()
        delSvgInteractivity()
        if(current_arrow_state !== ARROW_STATE[1]) {
            current_arrow_state = ARROW_STATE[1]
            setCSSBtnSelected('#btn_add_node')
            addSvgInteractivity()
        } else
            current_arrow_state = ARROW_STATE[0]
    }
    function onBtnAddEdgeClick(e) {
        setCSSAllNormal()
        delSvgInteractivity()
        if(current_arrow_state !== ARROW_STATE[2]) {
            current_arrow_state = ARROW_STATE[2]
            setCSSBtnSelected('#btn_add_edge')
            setCSSAllNodeAddEdge()
            addSvgInteractivity()
        } else
            current_arrow_state = ARROW_STATE[0]
    }
    function onBtnDeleteClick(e) {
        setCSSAllNormal()
        delSvgInteractivity()
        if(current_arrow_state !== ARROW_STATE[3]) {
            current_arrow_state = ARROW_STATE[3]
            setCSSBtnSelected('#btn_delete')
            setCSSAllEdgeDelete(true)
            addSvgInteractivity()
        } else
            current_arrow_state = ARROW_STATE[0]
    }
    function setBtnCSSAllNormal() {
        setCSSBtnNormal('#btn_add_node')
        setCSSBtnNormal('#btn_add_edge')
        setCSSBtnNormal('#btn_delete')
    }
    $('#btn_add_node').bind('click', onBtnAddNodeClick)
    $('#btn_add_edge').bind('click', onBtnAddEdgeClick)
    $('#btn_delete').bind('click', onBtnDeleteClick)

    function onSvgMouseDown(e) {
        let baseP = $svg.offset()
        if(current_arrow_state === ARROW_STATE[1])
            addNewNode(e.clientX - baseP.left, e.clientY - baseP.top)
    }
    function addSvgInteractivity() {
        $svg
            .css({cursor: 'crosshair'})
            .bind('mousedown', onSvgMouseDown)
    }
    function delSvgInteractivity() {
        $svg
            .css({cursor: 'default'})
            .unbind('mousedown', onSvgMouseDown)
    }

    function adjustEdgePosition(shape) {
        let nodePair = _edges.get(shape)
        let node1 = nodePair.node1
        let node2 = nodePair.node2
        let p1 = cutout(node1.position, node2.position, NODE_RADIUS)
        let p2 = cutout(node2.position, node1.position, NODE_RADIUS)
        shape.vertices[0].set(p1.x, p1.y)
        shape.vertices[1].set(p2.x, p2.y)
    }

    function onNodeMove(shape) {
        let edges = _nodes.get(shape).adjacencyEdges
        let text = _nodes.get(shape).text
        text.position.set(shape.position.x, shape.position.y)
        edges.forEach((v) => {
            adjustEdgePosition(v)
        })
    }

    function addNewNode(x, y) {
        let circle = two.makeCircle(x, y, NODE_RADIUS);
        circle.fill = 'rgb(0, 200, 255)';
        circle.stroke = 'grey';
        circle.linewidth = 2;

        let text = two.makeText(`P${node_count}`, x, y)
        node_count += 1

        two.update()

        let edges = {
            adjacencyEdges: new Set(),
            text: text
        }
        _nodes.set(circle, edges)

        setCSSNodeNormal(circle)
        addInteractivity(circle, text)
        return circle
    }
    function delNode(shape) {
        let edges = _nodes.get(shape).adjacencyEdges
        let text = _nodes.get(shape).text
        edges.forEach((v) => {
            delEdge(v)
        })
        _nodes.delete(shape)
        two.remove(text)
        two.remove(shape)
    }

    function setCSSNodeNormal(shape) {
        let text = _nodes.get(shape).text
        $(text._renderer.elem).css({ cursor: 'pointer' })
        $(shape._renderer.elem).css({ cursor: 'pointer' })
    }
    function setCSSNodeAddEdge(shape) {
        let text = _nodes.get(shape).text
        $(text._renderer.elem).css({ cursor: 'crosshair' })
        $(shape._renderer.elem).css({ cursor: 'crosshair' })
    }
    function setCSSAllNodeNormal() {
        _nodes.forEach((v, k) => {
            setCSSNodeNormal(k)
        })
    }
    function setCSSAllNodeAddEdge() {
        _nodes.forEach((v, k) => {
            setCSSNodeAddEdge(k)
        })
    }
    function setCSSAllNormal() {
        setBtnCSSAllNormal()
        setCSSAllNodeNormal()
        setCSSAllEdgeDelete(false)
    }

    function cutout(v1, v2, len) {
        let v3 = new Two.Vector(0, 0)
        let ox = v2.x - v1.x
        let oy = v2.y - v1.y
        let dis = Two.Vector.distanceBetween(v1, v2)
        let ratio = len / dis
        v3.set(v2.x - ox*ratio, v2.y - oy*ratio)
        return v3
    }

    function setCSSAllEdgeDelete(isTrue) {
        _edges.forEach((v, k) => {
            if(isTrue)
                $(k._renderer.elem).css({ cursor: 'pointer' })
            else
                $(k._renderer.elem).css({ cursor: 'default' })
        })
    }

    function hasEdge(node1, node2) {
        let edges = _nodes.get(node1).adjacencyEdges
        edges.forEach((v) => {
            let shape2 = getPeerNode(v, node1)
            if(shape2 === node2)
                return true
        })
        return false
    }

    function getPeerNode(edge, node1) {
        let shape1 = _edges.get(edge).node1
        let shape2 = _edges.get(edge).node2
        if(shape1 === node1)
            return shape2
        if(shape2 === node1)
            return shape1
        return null
    }

    function addEdge(shape1, shape2) {
        if(hasEdge(shape1, shape2))
            return

        let p1 = cutout(shape1.position, shape2.position, NODE_RADIUS)
        let p2 = cutout(shape2.position, shape1.position, NODE_RADIUS)
        let line = two.makeLine(p1.x, p1.y, p2.x, p2.y)
        line.linewidth = 4
        line.opacity = 1
        line.stroke = 'grey'
        two.update()
        addEdgeInteractivity(line)

        let nodePair = {
            node1: shape1,
            node2: shape2,
        }
        let n1_name = _nodes.get(shape1).text.value
        let n2_name = _nodes.get(shape2).text.value
        let n1 = parseInt(n1_name.substr(1, n1_name.length-1))
        let n2 = parseInt(n2_name.substr(1, n2_name.length-1))
        if(n1 > n2) {
            nodePair.node1 = shape2
            nodePair.node2 = shape1
        }
        _edges.set(line, nodePair)
        _nodes.get(shape1).adjacencyEdges.add(line)
        _nodes.get(shape2).adjacencyEdges.add(line)
        return line
    }
    function delEdge(line) {
        let nodePair = _edges.get(line)
        let edges1 = _nodes.get(nodePair.node1)
        let edges2 = _nodes.get(nodePair.node2)
        if(edges1) edges1.adjacencyEdges.delete(line)
        if(edges2) edges2.adjacencyEdges.delete(line)
        _edges.delete(line)
        two.remove(line)
    }

    function addEdgeInteractivity(shape) {
        function onMouseDown(e) {
            e.preventDefault();
            // 删除边
            if(current_arrow_state === ARROW_STATE[3]) {
                delEdge(shape)
                return false
            }
            return true
        }
        function onMouseEnter(e) {
            e.preventDefault();
            shape.stroke = 'black'
        }
        function onMouseLeave(e) {
            e.preventDefault();
            shape.stroke = 'grey'
        }
        $(shape._renderer.elem)
            .bind('mousedown', onMouseDown)
            .bind('mouseenter', onMouseEnter)
            .bind('mouseleave', onMouseLeave)
    }

    function onBtnTranslateClick(e) {
        let nodes_str = '['
        _nodes.forEach((v, k) => {
            nodes_str += (v.text.value + ', ')
        })
        nodes_str = nodes_str.substr(0, nodes_str.length-2)
        nodes_str += ']'

        let edges = []
        _edges.forEach((v, k) => {
            edges.push(k)
        })
        edges.sort(function (a, b) {
            let a_pair = _edges.get(a)
            let b_pair = _edges.get(b)
            let a_n1_name = _nodes.get(a_pair.node1).text.value
            let a_n2_name = _nodes.get(a_pair.node2).text.value
            let b_n1_name = _nodes.get(b_pair.node1).text.value
            let b_n2_name = _nodes.get(b_pair.node2).text.value
            let a_n1 = parseInt(a_n1_name.substr(1, a_n1_name.length-1))
            let a_n2 = parseInt(a_n2_name.substr(1, a_n2_name.length-1))
            let b_n1 = parseInt(b_n1_name.substr(1, b_n1_name.length-1))
            let b_n2 = parseInt(b_n2_name.substr(1, b_n2_name.length-1))
            if(a_n1 < b_n1)
                return -1;
            if(a_n1 === b_n1) {
                if(a_n2 < b_n2)
                    return -1;
            }
            return 1;
        })
        let edges_str = ''
        let i = 1
        edges.forEach((v) => {
            let npair = _edges.get(v)
            let n1_name = _nodes.get(npair.node1).text.value
            let n2_name = _nodes.get(npair.node2).text.value
            edges_str += `${i}. reachablitity(${n1_name}, ${n2_name})\n`
            i += 1
        })

        let text =
            `# Subnets, count: ${_nodes.size}\n` +
            `${nodes_str}\n\n` +
            `# Reachabilities, count: ${_edges.size}\n` +
            `${edges_str}`
        $('#text_edit_box').text(text)
    }
    $('#btn_translate').bind('click', onBtnTranslateClick)

    function onBtnRenderClick(e) {
        let text = $('#text_edit_box').val()
        post('algorithm', {
            method: 'compute_network_graph',
            params: text
        }, callbackComputeNetworkGraph)
    }
    $('#btn_render').bind('click', onBtnRenderClick)

    function callbackComputeNetworkGraph(data) {
        console.log(data)
    }

    function post(path, data, callback) {
        $.get('csrf', function (csrf) {
            data.csrfmiddlewaretoken = csrf
            $.post(path, data, callback)
        })
    }

    function test() {
        let n1 = addNewNode(72, 100)
        let n2 = addNewNode(213, 100)
        addEdge(n1, n2)
    }
    test()
})
